
import sqlite3
import mysql.connector
from datetime import datetime
#引入数据库包
import pymysql


class CalenderDB:
    #Initialization constructor method
    def __init__(self,db_type="sqlite",db_name="personal_ai_assistant", **kwargs):
        if db_type == "sqlite":
            self.conn = sqlite3.connect(db_name)
        elif db_type =="mysql":
            self.conn = mysql.connector.connect(
                host=kwargs.get("host","localhost"),
                user=kwargs.get("user","root"),
                password=kwargs.get("password","root"),
                database=kwargs.get("database","personal_ai_assistant")
            )
        else:
            raise ValueError("Unsupported database type")
        self.cursor = self.conn.cursor()


    # Insert data function
    def insert_event(self,event):
        """Add a new data item"""
        try:
            sql = """
            insert into calender_events (user_id,title,description,location,start_time,end_time,remindertime,is_all_day,source,create_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on duplicate key update 
            user_id=values(user_id),
            title=values(title),
            description=values(description),
            location=values(location),
            start_time=values(start_time),
            end_time=values(end_time),
            remindertime=values(remindertime),
            is_all_day=values(is_all_day),
            source=values(source),
            create_at=values(create_at);
              """
            self.cursor.execute(sql, event)
        except sqlite3.integrityError:
            print(f"Insert data failed,'{event}' already existed ")

    # Delete data function
    def delete_event(self, event):
        """Delete a date item"""
        sql = """
        delete from calender_events where title = ?
        """
        self.cursor.execute(sql, event)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print(f"Already delete: {event}")
        else:
            print(f"No item: {event}")

    # Selete date function
    def find_event(self,**kwargs):
        """ we can use any fields and values to select data from specific table ,for example name = "apple",category="fruit"
         """
        if not kwargs:
            print("there is no enquire conditions")
            return []
        where_clause = "AND".join([f"{key}=?" for key in kwargs])
        values  = list(kwargs.values())
        sql = f"select * from calender_events where (where_clause);"
        self.cursor.execute(sql,values)
        return self.cursor.fetchall()


    def close_conn(self):
          slef.conn.close()

