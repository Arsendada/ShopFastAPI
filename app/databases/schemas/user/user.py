from typing import Optional, List
import re
from pydantic import BaseModel, EmailStr, ValidationError, validator


pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    password2: str
    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

    @validator('password')
    def password_correct(cls, v):
        if re.match(pattern, v) is None:
            raise ValueError('Password has incorrecr format.')
        return v


class UserBaseInDB(UserBase):
    id: int


class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    hashed_password: str
    is_active: bool
    is_superuser: bool