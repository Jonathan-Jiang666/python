from dataclasses import dataclass

#Create a User DTO（Data Transfer Object）
class UserCreatDTO(BaseModle):
    username: str | None
    email: str | None
    passwordhash: str | None
    phonenumber: str| None
