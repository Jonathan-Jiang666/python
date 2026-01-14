# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column , Integer , String , func , DateTime, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base


class AIEmailAttachments (Base):
    __tablename__ = "ai_email_attachments"
    id = Column (Integer, primary_key=True , autoincrement=True)
    email_id = Column(Integer, ForeignKey("ai_email.email_id"), nullable=False)
    attachment_name = Column(String(200))
    attachment_path = Column(String(500))
    attachment_size = Column(Integer, index=True)
    attachment_type = Column(String(50))
    upload_time = Column(DateTime, server_default=func.now())
    attachment_content = Column(LargeBinary, index=True)
