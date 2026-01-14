
import sqlite3
import mysql.connector
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CalenderDB:
    # Initialization constructor method
    def __init__(self, db_type="sqlite", db_name="personal_ai_assistant", **kwargs):
        if db_type == "sqlite":
            self.conn = sqlite3.connect(db_name)
        elif db_type == "mysql":
            self.conn = mysql.connector.connect(
                host=kwargs.get("host", "localhost"),
                user=kwargs.get("user", "root"),
                password=kwargs.get("password", "root"),
                database=kwargs.get("database", "personal_ai_assistant"),
            )
        else:
            raise ValueError("Unsupported database type")
        self.cursor = self.conn.cursor()

    # Insert data function
    def insert_event(self, event):
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
        except sqlite3.IntegrityError:
            logger.warning("Insert data failed, '%s' already existed", event)

    # Delete data function
    def delete_event(self, event):
        """Delete a date item"""
        sql = """
        delete from calender_events where title = ?
        """
        self.cursor.execute(sql, event)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            logger.info("Already delete: %s", event)
        else:
            logger.info("No item: %s", event)

    # Select data function
    def find_event(self, **kwargs):
        """Use kwargs to select rows from calender_events table"""
        if not kwargs:
            logger.info("there is no enquire conditions")
            return []
        where_clause = " AND ".join([f"{key}=?" for key in kwargs])
        values = list(kwargs.values())
        sql = f"select * from calender_events where {where_clause};"
        self.cursor.execute(sql, values)
        return self.cursor.fetchall()


    def close_conn(self):
        self.conn.close()

