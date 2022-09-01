from enum import Enum
from pydantic import BaseModel, Field


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


class Gender(str, Enum):
    Select = 'Select'
    Male = 'Male'
    Female = 'Female'


class Profile(BaseModel):
    name: str
    phone: str
    gender: Gender = Field(None, alias='gender')

    class Config():
        orm_mode = True


class BaseProfile(Profile):
    profile_photo: str
    owner: ShowUser

    class Config():
        orm_mode = True
