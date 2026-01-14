from PersonalAIassistant.app.models_oma.calendar_events_bean import CalendarEvent
from PersonalAIassistant.app.database.db import Base, engine, SessionLocal
from sqlalchemy import and_
from datetime import datetime, date, timedelta


class CalenderEventsDataProcess:
    def __init__(self):
        print ("Init CalendarEventsDataProcess")
        Base.metadata.create_all (bind=engine)
        self.session = SessionLocal ()
        print ("导入成功，数据库连接可用")
        self.session.close ()

    # Insert a new data
    def insert_calender_Event(self , calenderEvent: CalendarEvent):
        # existing = self.session.query (CalendarEvent).filter_by (description=calenderEvent.description).first()  pay attention about the filter_by function adn filter function
        existing = self.session.query (CalendarEvent).filter ( and_(
                CalendarEvent.description == calenderEvent.description ,
                CalendarEvent.title == calenderEvent.title
            )
        ).first()
        if existing:
            return existing.id
        self.session.add(calenderEvent)
        self.session.commit()
        self.session.refresh(calenderEvent)
        return calenderEvent.id

    # Select Data by title
    def get_calender_event_by_title ( self , title: str ):
        return self.session.query (CalendarEvent).filter (CalendarEvent.title == title).first ()


    # Select Data by time
    def get_calender_event_by_time(self , time):
        return self.session.query (CalendarEvent).filter (CalendarEvent.start_time > time).all()

    # Get user by username
    def get__calender_event_by_userId(self , userid: int):
        return self.session.query (CalendarEvent).filter (CalendarEvent.user_id == userid).first ()

    # Update data by username
    def update_calender_event(self , title: str , updates: dict):
        calenderEvent = self.session.query (CalendarEvent).filter_by (title=title).first ()
        if not calenderEvent:
            return None
        for key , value in updates.items ():
            setattr (calenderEvent , key , value)
        self.session.commit ()
        self.session.refresh (calenderEvent)
        return calenderEvent

    # Delete a piece data by title
    def delete_calender_event_by_title(self , title: str):
        calenderEvent = self.session.query (CalendarEvent).filter_by (title=title).first ()
        if not calenderEvent:
            return False
        self.session.delete (calenderEvent)
        self.session.commit ()
        return True

    def close(self):
        if hasattr (self , 'session'):
            self.session.close ()
