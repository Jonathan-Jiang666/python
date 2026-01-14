# Column ：be used to define the table fiedls in the database
# Integer,String,DataTime: indicating the data type of the field
# func,provide support for SQL functions
# Base, it's the previously defined basic class of the ORM
from sqlalchemy import Column , Integer , String , func , DateTime
from sqlalchemy.ext.declarative import _declarative_base
from PersonalAIassistant.app.database.db import Base


class CourseSchedule (Base):
    __tablename__ = "course_schedule"
    id = Column (Integer , primary_key=True , index=True)
    user_id = Column (Integer , nullable=False , index=True)
    course_name = Column (String (255) , nullable=False , index=True)
    course_code = Column (String (100) , nullable=False , index=True)
    instructor = Column (String (100) , index=True)
    start_time = Column (DateTime , server_default=func.now ())
    end_time = Column (DateTime , server_default=func.now ())
    location = Column (String (100) , index=True)
    notes = Column (String (100000))
