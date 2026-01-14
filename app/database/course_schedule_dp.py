import os            # file path method
import pickle        # sequence and anti-sequence object
import json          # Json document process
import base64        # Base64 encode
import logging       # Log record
import datetime      # Date and time process
from PersonalAIassistant.app.database.db import Base, engine, SessionLocal
from PersonalAIassistant.app.models_oma.course_schedule_bean import CourseSchedule


class CourseScheduleDataProcess:


    def __init__(self):
        print ("Initial CourseScheduleDataProcess")
        Base.metadata.create_all (bind=engine)
        self.session = SessionLocal()
        print ("导入成功，数据库连接可用")
        #self.session.close ()



    # Insert a new data
    def insert_email ( self , course: CourseSchedule ):
        existing = self.session.query (CourseSchedule).filter_by (course_name=course.course_name).first()
        if existing:
            return existing.id
        self.session.add(course)
        self.session.commit()
        self.session.refresh(course)
        return course.id

    # Select Data by time
    def get_course_schedule_by_time (self, time ):
        return self.session.query (CourseSchedule).filter (CourseSchedule.start_time > time).all ()


     # Select all courses
    def get_all_courses(self):
        return self.session.query(CourseSchedule).all()



    # Select Data by course_name
    def get_user_by_id(self, course_name: str):
        return self.session.query(CourseSchedule).filter(CourseSchedule.course_name == course_name).first()


    # Select Data by course_code
    def get_user_by_email(self, code: str):
        return self.session.query(CourseSchedule).filter(CourseSchedule.course_code == code).first()


