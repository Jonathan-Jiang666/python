# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column, Integer, String, func, DateTime, Float
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base
class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100))
    weather_date = Column(DateTime, server_default=func.now())
    temperature_high = Column(Float)
    conditions = Column(String(100))
    wind_speed = Column(Float)
    humidity = Column(Integer)
    precipitation_probability = Column(Float)