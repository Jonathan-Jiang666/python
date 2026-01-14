from PersonalAIassistant.app.models_oma.weather_data_bean import WeatherData
from PersonalAIassistant.app.database.db import Base, engine, SessionLocal
from datetime import datetime, date, timedelta


class WeatherDataProcess:
    def __init__(self):
        print ("Init WeatherDataProcess")
        Base.metadata.create_all (bind=engine)
        self.session = SessionLocal ()
        print ("导入成功，数据库连接可用")
        #self.session.close ()


    # Insert a new data
    def insert_weather(self, weather: WeatherData ):
        existing = self.session.query( WeatherData).filter_by (weather_date = weather.weather_date).first ()
        if existing:
            return existing.id
        self.session.add (weather)
        self.session.commit ()
        self.session.refresh (weather)
        return weather.id


    # Select Data by time
    def get_weather_data_by_time(self, time ):
        return self.session.query (WeatherData).filter (WeatherData.weather_date> time).all ()
