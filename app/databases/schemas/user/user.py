from typing import Optional
import re
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)


class UserCreate(UserBase):
    password: str = Field(...)

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


class UserUpdate(BaseModel):
    username: str


class UserInDB(UserBaseInDB):
    created_at: datetime
    updated_at: datetime
    hashed_password: str
    is_active: bool
    is_superuser: bool