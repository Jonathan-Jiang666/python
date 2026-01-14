from db import database, UserORM, engine, Base
from models import Users


# Create an User table if the table is not existence
# Base.metadata.create_all(bing=engine)

def main():
    #Connect the database
    db = SessionLocal()

    # Create a new User
    print("Create a new User")

    user = UserORM.insert_user(db, "Jonathan", "jiangmaokun15@gmail.com")
    print("Created:", user.id, user.name, user.email)

    # Selece all users
    print("Select all users")
    users = UserORM.get_users(db)
    for u in users:
        print(f"Username is", {u.name})

    # Update User information
    print("Update user's email")
    update = UserORM.update_user_email(db, user.id, "kunzi@126.com")

    # Delete a user
    UserORM.delete_user(db, user.id)

    db.close()
