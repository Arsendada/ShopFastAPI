from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    username: str


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: str
    password: str


class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    hashed_password: str