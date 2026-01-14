import logging

logger = logging.getLogger(__name__)


def main():
    # Connect the database
    db = SessionLocal()

    # Create a new User
    logger.info("Create a new User")

    user = UserORM.insert_user(db, "Jonathan", "jiangmaokun15@gmail.com")
    logger.info("Created: %s %s %s", user.id, user.name, user.email)

    # Select all users
    logger.info("Select all users")
    users = UserORM.get_users(db)
    for u in users:
        logger.info("Username is %s", u.name)

    # Update User information
    logger.info("Update user's email")
    update = UserORM.update_user_email(db, user.id, "kunzi@126.com")

    # Delete a user
    UserORM.delete_user(db, user.id)

    db.close()
