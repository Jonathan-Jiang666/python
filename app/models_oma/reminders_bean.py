# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column, Integer, String, func, DateTime, DECIMAL, Float
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base
class Reminders(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=Float, index=True)
    due_date = Column(DateTime, server_default=func.now())
    is_completed = Column(Integer)
    priority = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())