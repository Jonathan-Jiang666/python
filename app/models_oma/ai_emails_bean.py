# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column , Integer , String , func , DateTime, Text
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base


class AIEmails (Base):
    __tablename__ = "ai_emails"
    email_id = Column (Integer , primary_key=True , autoincrement=True,index=True)
    user_id = Column (Integer , nullable=True , index=True)
    email_title = Column (Text , nullable=False , index=True)
    email_priority_type = Column (String (50) , nullable=False , index=True)
    email_content = Column (Text , nullable=False , index=True)
    email_from = Column (Text , nullable=False , index=True)
    email_to = Column (Text , nullable=False , index=True)
    email_time = Column (DateTime , server_default=func.now ())
