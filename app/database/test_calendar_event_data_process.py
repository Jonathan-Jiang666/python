import unittest
from CalendarEventsDP import CalenderEventsDataProcess
from PersonalAIassistant.app.models_oma.calendar_events_bean import CalendarEvent


class TestCalendarEventDataProcess (unittest.TestCase):
    def setUp(self):
        self.db = CalenderEventsDataProcess ()

    def tearDown(self):
        # Close the database connection
        if hasattr (self.db , "close"):
            self.db.close ()

    # Add a new piece data
    def test_insert_calendar_event(self):
        calendar_event = CalendarEvent (user_id=1 , title="test" , description="1111111111" , location="Galway" ,
                                        is_all_day=1 , source="iphone")
        calendar_event_id = self.db.insert_calender_Event (calendar_event)
        self.assertIsNotNone (calendar_event_id)

        # If insert the same data information return the same data ID
        duplicate_id = self.db.insert_calender_Event (calendar_event)
        self.assertEqual (calendar_event_id , duplicate_id)

    # Update a piece data
    # def test_update_calender_event(self):
    #    print("ccccc")
    #   # Firstly , insert a piece dato to users table
    #    user = PersonalAIassistant.app.models_oma.Users.Users(username="test", email="old@example.com", password_hash="123456" , phone_number="1110000")
    #    self.db.insert_user(user)

    #    # And then update some informatoin for the same user
    #   updated_user = self.db.update_user("test", {"email": "new@example.com"})

    # self.assertIsNone(updated_user)
    #   self.assertEqual(updated_user.email, "new@example.com")

    # def test_delete_user(self):
    #   print("ddddd")
    #   user = PersonalAIassistant.app.models_oma.Users.Users(username="Wang", email="w@example.com", password_hash="123456" , phone_number="111222")
    #   self.db.insert_user(user)

    #   retult = self.db.delete_user_by_name("Wang")
    #   self.assertTrue(retult)

    # And then select again from table
    #   user = self.db.get_user_by_username("Wang")
    #   self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main ()
