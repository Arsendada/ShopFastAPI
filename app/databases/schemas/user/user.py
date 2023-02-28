from typing import Optional
import re
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)


class UserCreate(UserBase):
    password: str = Field(...)
    password2: str = Field(...)
    # @validator('password2')
    # def password_match(cls, v, values, **kwargs):
    #     if 'password' in values and v != values['password']:
    #         raise ValueError('passwords do not match')
    #     return v
    #
    # @validator('password')
    # def password_correct(cls, v):
    #     pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)' \
    #               r'(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    #
    #     if re.match(pattern, v) is None:
    #         raise ValueError('Password has incorrect format.')
    #     return v

    class Config:
        orm_mode = True
        schema_extra = {
            "email": "test@gmail.com",
            "username": "Arsen",
            "password": "!Arf45457h",
            "password2": "!Arf45457h",
        }


class UserBaseInDB(UserBase):
    id: int


class UserUpdate(UserCreate):
    old_password: str = Field(...)


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    hashed_password: str
    is_active: bool
    is_superuser: bool