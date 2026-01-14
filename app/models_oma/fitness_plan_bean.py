# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column, Integer, String, func, DateTime, DECIMAL
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base
class FitnessPlan(Base):
    __tablename__ = "fitness_plan"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    session_type = Column(String(100))
    session_date = Column(DateTime, server_default=func.now())
    target_steps = Column(Integer)
    target_calories = Column(Integer)
    target_minutes = Column(Integer)
    heart_rate_zone = Column(String(50))
    calories_bumed = Column(DECIMAL)
    notes = Column(String(100000))
    created_at = Column(DateTime, server_default=func.now())