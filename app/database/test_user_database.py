import unittest
import PersonalAIassistant.app.models_oma.users_bean
from UserDataProcess import UserDataProcess
import PersonalAIassistant.app.database.user_data_process as udp

print ("UserDataProcess load from" , udp.__file__)


class TestUserDatabase (unittest.TestCase):
    def setUp(self):
        print ("aaaaa")
        # self.db = UserDataProcess(
        #    host="localhost",
        #    user="root",
        #    password="root",
        #    database="personal_ai_assistant"
        # )

        # self.db.delete_user(self.test_user["username"])

        # Initialize database connection
        # self.db = UserDataProcess(user="root", password="root", host="localhost://3306", database="personal_ai_assistant")

        self.db = UserDataProcess ()

    def tearDown(self):
        # Close the database connection
        if hasattr (self.db , "close"):
            self.db.close ()

    # Add a new piece data
    def test_insert_user(self):
        print ("bbbbb")
        user = PersonalAIassistant.app.models_oma.users_bean.Users (username="test" , email="test@example.com" ,
                                                                    password_hash="123456" , phone_number="1110000")
        user_id = self.db.insert_user (user)
        self.assertIsNotNone (user_id)

        # If insert the same user information return the same User ID
        duplicate_id = self.db.insert_user (user)
        self.assertEqual (user_id , duplicate_id)

    # Update a piece data
    def test_update_email(self):
        print ("ccccc")
        # Firstly , insert a piece dato to users table
        user = PersonalAIassistant.app.models_oma.users_bean.Users (username="test" , email="old@example.com" ,
                                                                    password_hash="123456" , phone_number="1110000")
        self.db.insert_user (user)

        # And then update some informatoin for the same user
        updated_user = self.db.update_user ("test" , {"email": "new@example.com"})

        # self.assertIsNone(updated_user)
        self.assertEqual (updated_user.email , "new@example.com")

    def test_delete_user(self):
        print ("ddddd")
        user = PersonalAIassistant.app.models_oma.users_bean.Users (username="Wang" , email="w@example.com" ,
                                                                    password_hash="123456" , phone_number="111222")
        self.db.insert_user (user)

        retult = self.db.delete_user_by_name ("Wang")
        self.assertTrue (retult)

        # And then select again from table
        user = self.db.get_user_by_username ("Wang")
        self.assertIsNone (user)


if __name__ == "__main__":
    unittest.main ()
