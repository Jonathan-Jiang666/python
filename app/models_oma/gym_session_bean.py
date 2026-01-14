# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column, Integer, String, func, DateTime, DECIMAL
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base
class GymSession(Base):
    __tablename__ = "gym_session"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    session_date = Column(DateTime, server_default=func.now())
    start_time = Column (DateTime , server_default=func.now ())
    end_time = Column (DateTime , server_default=func.now ())
    duration_minutes = Column(Integer)
    focus_area = Column(String(50))
    heealth_data_i = Column(Integer)