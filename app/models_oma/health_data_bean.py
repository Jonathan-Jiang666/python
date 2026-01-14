# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column, Integer, String, func, DateTime, DECIMAL, Float
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base
class HealthData(Base):
    __tablename__ = "health_data"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    steps = Column(Integer)
    distance_km = Column(Integer)
    exercise_minutes = Column(Integer)
    sleep_hours = Column(Float)
    avg_heart_rate = Column(Integer)
    rest_heart_rate = Column(Integer)
    weight = Column(Float)
    calories_bumed = Column(DECIMAL)
    data_source = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())