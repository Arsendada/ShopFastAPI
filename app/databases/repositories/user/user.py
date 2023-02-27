from app.core.security import get_password_hash
from app.databases.repositories.base import BaseCrud
from app.databases.models.user.user import User
from app.databases.schemas.user.user import UserInDB, UserCreate


class UserCrud(BaseCrud):

    async def get_user(self, user_id: int):
        result = await self.sess.get(User, user_id)
        return result

    async def is_active(self, user: UserInDB) -> bool:
        return user.is_active

    async def is_superuser(self, user: UserInDB) -> bool:
        return user.is_superuser

    async def create_user(self, user: UserCreate):
        new_user_data = user.dict()
        password = new_user_data.pop('password')
        new_user_data["hashed_password"] = get_password_hash(password)
        result = User(new_user_data)
        await self.sess.add(result)
        await self.sess.commit()
        await self.sess.refresh(result)
        return result

