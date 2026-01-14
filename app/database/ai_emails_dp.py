import os            # file path method
import pickle        # sequence and anti-sequence object
import json          # Json document process
import base64        # Base64 encode
import logging       # Log record
import datetime      # Date and time process
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from PersonalAIassistant.app.database.db import Base, engine, SessionLocal
from PersonalAIassistant.app.models_oma.ai_emails_bean import AIEmails
from email.utils import parsedate_to_datetime

# Logging level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # log format
    handlers=[logging.FileHandler("gmail_fetcher.log"), logging.StreamHandler()]  # output to document and console
)


class AIEmailDataProcess:
    """Gmail API email fetcher and processor"""
    # Gmail API邮件获取器和处理器

    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']   #API permisson scope
        self.credentials_file = credentials_file  # Google API credential file# API权限范围（只读）
        self.token_file = token_file   # Authentication token cache file # 认证token缓存文件
        self.service = None   # Gmail Service Users# Gmail服务对象
        self.processed_emails = set() ## Set of Processed Email IDs# 已处理邮件ID集合
        self.load_processed_emails() ## Loading processed email records# 加载已处理的邮件记录

        print ("Initial AIEamilDataProcess")
        Base.metadata.create_all (bind=engine)
        self.session = SessionLocal ()
        print ("导入成功，数据库连接可用")
        #self.session.close ()


    def get_email_service(self):
        """Initialize Gmail API service"""
        creds = None
        # 检查 token 文件 # Check if a token file already exists
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token) ##加载已保存的凭证

        # 没有有效凭证就重新授权
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # 首次授权流程
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(f"credentials file not found: {self.credentials_file}")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0) # 本地服务器方式授权
            # 保存新的token
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        # 构建Gmail API服务
        self.service = build('gmail', 'v1', credentials=creds)
        return self.service

    def load_processed_emails(self):
        """Load already processed emails from JSON"""
        """从JSON文件加载已处理的邮件ID"""
        self.processed_emails = set()
        try:
            if os.path.exists('processed_emails.json'):
                with open('processed_emails.json', 'r') as f:
                    self.processed_emails = set(json.load(f))
        except Exception as e:
            logging.warning(f"Failed to load processed emails: {e}")

    def save_processed_emails(self):
        """Save processed emails to JSON"""
        """保存已处理的邮件ID到JSON文件"""
        try:
            with open('processed_emails.json', 'w') as f:
                json.dump(list(self.processed_emails), f)
        except Exception as e:
            logging.error(f"Failed to save processed emails: {e}")




    # Using Google API to get all email data
    def get_all_emails(self, days_back=100):
        """Get all emails from last N days"""
        if not self.service:
            self.get_email_service()  # 确保服务已初始化

        try:
            # 计算查询日期（30天前）
            after_date = (datetime.datetime.now() - datetime.timedelta(days=days_back)).strftime('%Y/%m/%d')
            query = f'after:{after_date}'  # Gmail搜索查询语法
            all_messages = []
            page_token = None

            # 分页获取所有邮件（Gmail API限制每页500条）
            while True:
                response = self.service.users().messages().list(
                    userId='me', # 当前用户
                    q=query, # 搜索条件
                    pageToken=page_token,# 分页token
                    maxResults=500 # 每页最大结果数
                ).execute()

                messages = response.get('messages', [])
                all_messages.extend(messages)

                page_token = response.get('nextPageToken')
                if not page_token: # 没有下一页时退出循环
                    break

            logging.info(f"✅ Found {len(all_messages)} emails in the last {days_back} days.")
            return all_messages

        except Exception as e:
            logging.error(f"❌ Error fetching emails: {e}")
            return []

    def get_message_details(self, message_id):
        """Get full message details"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full' # 获取完整邮件内容
            ).execute()
            return message
        except Exception as e:
            logging.error(f"Failed to get message {message_id}: {e}")
            return None

    def parse_message(self, message):
        """Extract email content"""
        try:
            headers = message['payload'].get('headers', [])
            # 从邮件头提取关键信息
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            recipient = next((h['value'] for h in headers if h['name'] == 'To'), '')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
            message_id = next((h['value'] for h in headers if h['name'] == 'Message-ID'), '')

            # 提取邮件正文
            body = self.extract_body(message['payload'])

            return {
                'id': message['id'],  # Gmail内部ID
                'message_id': message_id, # 邮件Message-ID
                'subject': subject, # 邮件主题
                'sender': sender, # 发件人
                'recipient': recipient, #接收人
                'date': date, # 发送日期
                'body': body, # 邮件正文
                'snippet': message.get('snippet', ''), # 邮件摘要
                'internalDate': message.get('internalDate', ''), # 内部时间戳
                'labelIds': message.get('labelIds', []) # 标签ID列表
            }
        except Exception as e:
            logging.error(f"Failed to parse message: {e}")
            return None

    def extract_body(self, payload):
        """Extract plain text body from payload"""

        body = ""
        if 'parts' in payload: # 多部分邮件（常见）
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain' and 'data' in part['body']:
                    # 找到纯文本部分并解码
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
                elif part.get('mimeType') == 'multipart/alternative':
                    # 递归处理嵌套的多部分邮件
                    body = self.extract_body(part)
                    if body:
                        break
        else:
            # 单部分邮件
            if payload.get('mimeType') == 'text/plain' and 'data' in payload.get('body', {}):
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')

        return body

    def run(self, days_back: int):
        """Main execution"""
        self.get_email_service() # 初始化服务
        emails = self.get_all_emails(days_back) # 获取邮件列表
        for msg in emails:
            msg_id = msg['id']
            if msg_id in self.processed_emails: # 跳过已处理的邮件
                continue
            message = self.get_message_details(msg_id)  # 获取邮件详情
            if message:
                parsed = self.parse_message(message)  # 解析邮件
                if parsed:
                    date_str = parsed.get ("date" , None)
                    if date_str:
                        try:
                            trigger_time = parsedate_to_datetime (date_str)
                        except Exception:
                            trigger_time = datetime.datetime.utcnow ()
                    else:
                        trigger_time = datetime.datetime.utcnow ()

                    # TODO: save to DB
                    email  = AIEmails(
                        user_id =1,
                        email_title=parsed.get("subject","No Subject"),
                        email_priority_type=parsed.get("priority","Normal"),
                        email_content=parsed.get("body",""),
                        email_from=parsed.get("from",""),
                        email_to = parsed.get("recipient",""),
                        email_time=trigger_time
                    )
                    self.insert_email(email)
                    logging.info(f"Processed email: {parsed['subject']}")
                    self.processed_emails.add(msg_id) # 标记为已处理
        self.save_processed_emails() # 保存处理记录
        logging.info("🎉 Email data processing completed.")




    # Insert a new data
    def insert_email(self, email: AIEmails):
        existing = self.session.query(AIEmails).filter_by(email_title=email.email_title).first()
        if existing:
            return existing.email_id
        self.session.add(email)
        self.session.commit()
        self.session.refresh(email)
        return email.email_id

    # Select Data by email_title
    def get_user_by_id(self, title: str):
        return self.session.query(AIEmails).filter(AIEmails.email_title == title).first()

    # Select Data by email
    def get_user_by_email(self, email: str):
        return self.session.query(Users).filter(Users.email == email).first()

    # Get user by email_to
    def get_user_by_username(self, email_to: str):
        return self.session.query(AIEmails).filter(AIEmails.email_to == email_to).first()

    # Update data by email_title
    def update_email(self, email_title: str, updates: dict):
        email = self.session.query(AIEmails).filter_by(email_title=email_title).first()
        if not email:
            return None
        for key, value in updates.items():
            setattr(email, key, value)
        self.session.commit()
        self.session.refresh(email)
        return email

    # Get emails greater by email_time
    def get_emails_by_emailtime( self, since_time ):
        return self.session.query(AIEmails).filter(AIEmails.email_time > since_time).all()

if __name__ == '__main__':
    processor = AIEmailDataProcess(
        credentials_file='credentials.json',
        token_file='token.pickle'
    )
    processor.run(days_back=600)
    processor.session.close()
