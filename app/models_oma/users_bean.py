# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    password_hash = Column(String(255), nullable=False, index=True)
    phone_number = Column (String(55), unique=True, index=True)
