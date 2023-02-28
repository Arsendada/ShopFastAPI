from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import select

from app.core import settings
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.databases.repositories.base import BaseCrud
from app.databases.models.user.user import User
from app.databases.schemas.user.user import UserInDB


class LoginCrud(BaseCrud):
    async def get(self, user_id: int | None):
        result = await self.sess.get(User, user_id)
        print(result)
        return result

    async def get_by_email(self, email: str):
        stmt = (select(User).where(User.email == email))
        result = await self.sess.execute(stmt)
        result = result.scalar_one_or_none()
        if result:
            return UserInDB(**result.__dict__)
        return result


    async def authenticate(self, *, email: str,
                           password: str,):
        user = await self.get_by_email(email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=404, detail="Incorrect email or password.")
        elif not self.is_active(user):
            raise HTTPException(status_code=400, detail="Inactive user")
        access_token_expires = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                data={"user_id": user.id},
                expires_delta=access_token_expires),
            "token_type": "bearer",}

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_admin