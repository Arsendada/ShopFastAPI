from fastapi import HTTPException
from sqlalchemy import select

from app.core.security import get_password_hash
from app.databases.repositories.base import BaseCrud
from app.databases.models.user.user import User
from app.databases.schemas.user.user import UserInDB, UserCreate


class UserCrud(BaseCrud):

    async def get_by_email(self, email: str):
        stmt = (select(User).where(User.email == email))
        result = await self.sess.execute(stmt)
        return result.scalar_one_or_none()

    async def is_active(self, user: UserInDB) -> bool:
        return user.is_active

    async def is_superuser(self, user: UserInDB) -> bool:
        return user.is_superuser

    async def create_user(self, user: UserCreate):
        check_email = await self.get_by_email(email=user.email)
        if check_email:
            raise HTTPException(status_code=404, detail="User already exist.")
        new_user_data = user.dict()
        del new_user_data['password2']
        password = new_user_data.pop('password')
        new_user_data["hashed_password"] = get_password_hash(password)
        result = User(**new_user_data)
        self.sess.add(result)
        await self.sess.commit()
        await self.sess.refresh(result)
        return result

