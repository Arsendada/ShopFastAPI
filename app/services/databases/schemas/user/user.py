import re
from pydantic import BaseModel, EmailStr, Field, validator

from app.services.databases.schemas.base import BaseInDB


class UserPasswordDTO(BaseModel):
    password: str = Field(...)

    @validator('password')
    def password_correct(cls, v):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)' \
                  r'(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        if re.match(pattern, v) is None:
            raise ValueError('Password has incorrect format.')
        return v

    class Config:
        orm_mode = True
        schema_extra = {
            "password": "!Arf45457h",
        }


class UserBase(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)


class UserCreateDTO(UserBase, UserPasswordDTO):
    class Config:
        orm_mode = True
        schema_extra = {
            "email": "test@gmail.com",
            "username": "Arsen",
            "password": "!Arf45457h",
        }


class UserUpdateDTO(BaseModel):
    username: str

    class Config:
        orm_mode = True
        schema_extra = {
            "username": "Paul",
        }


class UserInDB(UserBase, BaseInDB):
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "created_at": "2023-04-02 22:03:21.605901 +00:00",
            "updated_at": "2023-04-02 22:03:21.605901 +00:00",
            "email": "test@gmail.com",
            "username": "Arsen",
        }
