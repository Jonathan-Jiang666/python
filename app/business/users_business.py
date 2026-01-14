
from app.database.UserDataProcess import UserDataProcess


class UsersBusiness:
    def __init__(self):
        self.processor = UserDataProcess()

    def create_user(self, user_dto: UsersCreateDTO):
        # Directly convert the DTO into an ORM object
        user = Users(
            username=user.username,
            email=user.email,
            passwordhash=user.passwordhash,
            phonenumber=user.phonenumber
        )
        return self.insert_user(user)



#单独调试的方法
if __name__=="__main__":
    # step 1: Ready for creating an DTO
    user_dto= UserCreateDTO(
        username="Jonathan",
        email="123456@example.com",
        passwordhash="111111",
        phonenumber="871042222"
    )
    # step 2: Ready for a Repository
    repo = UserDataProcess()
    # step 3: Ready for a business example
    business  = UsersBusiness(repo)
    # step 4: Calling the buisness method
    result = business.create_user(user_dto)
    print("The result of insert:", result)


