from PersonalAIassistant.app.models_oma.users_bean import Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base , engine , SessionLocal
import mysql.connector


class UserDataProcess:
    def __init__(self):
        Base.metadata.create_all (bind=engine)
        self.session = SessionLocal ()
        print ("导入成功，数据库连接可用")
        self.session.close ()

        # def __int__(self, user, password, host, database):
        """
           Initialize database connection and Session
        """
        # Assemble the database URL
        # user = "root",
        # password = "root",
        # host = "localhost",
        # database = "personal_ai_assistant"
        # db_url = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'

        # Create Engine
        # self.engine = create_engine(db_url, echo=True)  # echo=True can print the SQL

        # Create Session class
        # self.Session = sessionmaker(bind=self.engine)

        # Create session object
        # self.session = Session()

    # def __init__(self, host="localhost", user="root", password="root", database="personal_ai_assistant"):
    #    """初始化数据库连接"""
    #    self.conn = mysql.connector.connect(
    #        host=host,
    #        user=user,
    #        password=password,
    #        database=database
    #    )
    #    self.cursor = self.conn.cursor(dictionary=True)

    # Insert a new data
    def insert_user(self , user: Users):
        existing = self.session.query (Users).filter_by (username=user.username).first ()
        if existing:
            return existing.id
        self.session.add (user)
        self.session.commit ()
        self.session.refresh (user)
        return user.id

    # Select Data by ID
    def get_user_by_id(self , id: int):
        return self.session.query (Users).filter (Users.id == id).first ()

    # Select Data by email
    def get_user_by_email(self , email: str):
        return self.session.query (Users).filter (Users.email == email).first ()

    # Get user by username
    def get_user_by_username(self , username: str):
        return self.session.query (Users).filter (Users.username == username).first ()

    # Update data by username
    def update_user(self , username: str , updates: dict):
        user = self.session.query (Users).filter_by (username=username).first ()
        if not user:
            return None
        for key , value in updates.items ():
            setattr (user , key , value)
        self.session.commit ()
        self.session.refresh (user)
        return user

    # Delete a piece data by username
    def delete_user_by_name(self , username: str):
        user = self.session.query (Users).filter_by (username=username).first ()
        if not user:
            return False
        self.session.delete (user)
        self.session.commit ()
        return True

    def close(self):
        if hasattr (self , 'session'):
            self.session.close ()
