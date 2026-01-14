# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column , Integer , String , func , DateTime
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base


class CalendarEvent (Base):
    __tablename__ = "calendar_events"
    id = Column (Integer , primary_key=True , index=True)
    user_id = Column (Integer , nullable=False , index=True)
    title = Column (String (255) , unique=True , nullable=False , index=True)
    description = Column (String (100000) , index=True)
    location = Column (String (255) , index=True)
    start_time = Column (DateTime , server_default=func.now ())
    end_time = Column (DateTime , server_default=func.now ())
    remindertime = Column (String (255) , index=True)
    is_all_day = Column (Integer , nullable=False)
    source = Column (String (50) , index=True)
    created_at = Column (DateTime , server_default=func.now ())
