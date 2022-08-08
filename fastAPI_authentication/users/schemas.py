from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode = True


class ChangePassword(BaseModel):
    new_password: str
    confirm_new_password: str

    class Config():
        orm_mode = True


class Profile(BaseModel):
    name: str
    phone: str
    gender: str

    class Config():
        orm_mode = True


class BaseProfile(Profile):
    profile_photo: str
    owner: ShowUser

    class Config():
        orm_mode = True
