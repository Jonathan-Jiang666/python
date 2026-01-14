import os
import sys

# =====Make sure that finding the root file path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ===== Import the business and data process layer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.business.UsersBusiness import UsersBusiness
from app.business.UserCreateDTO import UserCreateDTO
from app.database.UserDataProcess import UserDataProcess


def main():
    # === Creating a business data process object
    repo = UserDataProcess()
    # === Crating a business object
    business = UsersBusiness(repo)

    # step 1: Ready for creating an DTO
    user_dto = UserCreateDTO(
        username="Jonathan",
        email="123456@example.com",
        passwordhash="111111",
        phonenumber="871042222"
    )
    # step 2: Ready for a Repository
    repo = UserDataProcess()
    # step 3: Ready for a business example
    business = UsersBusiness(repo)
    # step 4: Calling the buisness method
    result = business.create_user(user_dto)
    print("The result of insert:", result)


if __name__ == "__main__":
    main()
