from datetime import timedelta
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.security.jwt import create_access_token
from app.services.security.password_security import verify_password
from app.core.settings import settings
from app.services.security.password_security import get_password_hash
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.models.user.user import User
from app.services.databases.schemas.user.user import UserInDB, UserCreate, UserUpdate


class UserCrud(BaseCrud):

    async def get(self, user_id: int) -> Optional[UserInDB]:
        result = await self.sess.get(User, user_id)
        print(result)
        return result

    async def get_by_email(self, email: str):
        stmt = (select(User).where(User.email == email))
        result = await self.sess.execute(stmt)
        return result.scalar()

    async def is_active(self, user: UserInDB) -> bool:
        return user.is_active

    async def is_superuser(self, user: UserInDB) -> bool:
        return user.is_superuser

    async def create_user(self, user: UserCreate) -> UserInDB:
        check_email = await self.get_by_email(email=user.email)
        if check_email:
            raise HTTPException(status_code=404, detail="User already exist.")
        new_user_data = user.dict()
        password = new_user_data.pop('password')
        new_user_data["hashed_password"] = get_password_hash(password)
        result = User(**new_user_data)
        self.sess.add(result)
        await self.sess.commit()
        await self.sess.refresh(result)
        return result

    async def authenticate(self, *, email: str,
                           password: str,):
        user = await self.get_by_email(email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=404, detail="Incorrect email or password.")
        elif not await self.is_active(user):
            raise HTTPException(status_code=400, detail="Inactive user")
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                data={"user_id": user.id},
                expires_delta=access_token_expires),
            "token_type": "bearer",}


    async def delete_user(self, user_id: int) -> bool:
        user = await self.get(user_id)
        if not user:
            return False
        await self.sess.delete(user)
        await self.sess.commit()
        return True

    async def update_user(self, user_id: int,
                          data: UserUpdate):
        stmt = (update(User).
                where(User.id == user_id).
                values(**data.dict()).
                returning(User))
        try:
            result = await self.sess.scalar(stmt)
            await self.sess.commit()
            await self.sess.refresh(result)
            return result
        except UnmappedInstanceError:
            return False

    async def password_change(self, user: UserInDB,
                             new_password: str) -> bool:
        new_password_hash = get_password_hash(new_password)
        setattr(user, 'hashed_password', new_password_hash)
        self.sess.add(user)
        await self.sess.commit()
        await self.sess.refresh(user)
        return True

    async def activate_user(self, user: UserInDB) -> bool:
        setattr(user, 'is_active', True)
        self.sess.add(user)
        await self.sess.commit()
        await self.sess.refresh(user)
        return True
