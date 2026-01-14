import unittest

from apscheduler.schedulers.blocking import BlockingScheduler
import logging

from PersonalAIassistant.app.business.calendar_event_data_fatory import CalendarEventDF
from PersonalAIassistant.app.models_oma.calendar_events_bean import CalendarEvent

logger = logging.getLogger(__name__)

class TestCalendarEventDataFatory (unittest.TestCase):


    def setUp(self):
       # obj = CalendarEventDF()
       pass  # If you dont wanna output any information , we can use "pass" placeholder

    def tearDown(self):
        # Close the database connection
        # if hasattr (self.db , "close"):
        #   self.db.close ()
        pass

    def test_download_original_data(self):
        obj = CalendarEventDF()
        calendars = obj.get_calendars ()
        calendarEvents = obj.original_calendar_data_process (calendars)
        logger.info("TestCalendarEvent account of array is %d", len(calendarEvents))
        obj.iteration_CalendarArray_To_Table(calendarEvents)
        self.job()

        #print("当前测试类获取到的事件数量是",len(calendarEvents))


if __name__ == "__main__":
        unittest.main()