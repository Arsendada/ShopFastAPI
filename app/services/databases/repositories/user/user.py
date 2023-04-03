from datetime import timedelta
from typing import Optional
from fastapi import HTTPException

from app.services.security.jwt import create_access_token
from app.services.security.password_security import verify_password
from app.core.settings import settings
from app.services.security.password_security import get_password_hash
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.models.user.user import User
from app.services.databases.schemas.user.user import UserInDB, UserCreate, UserUpdate


class UserCrud(BaseCrud):

    model = User

    async def get(
            self,
            user_id: int = None,
            email: str = None
    ) -> Optional[UserInDB]:
        if user_id:
            return await self._get(
                field=self.model.id,
                value=user_id
            )
        return await self._get(
            field=self.model.email,
            value=email
        )


    async def get_list_user(
            self,
            offset: int = 0,
            limit: int = 20
    ):
        return await self._get_list(
            limit=limit,
            offset=offset
        )

    async def create_user(
            self,
            data: UserCreate
    ) -> UserInDB:
        new_user_data = data.__dict__
        password = new_user_data.pop('password')
        new_user_data["hashed_password"] = get_password_hash(password)
        return await self._create(new_user_data)

    async def authenticate(
            self,
            email: str,
            password: str
    ):
        user = await self.get(email=email)

        if not user or not verify_password(password,
                                           user.hashed_password):
            raise HTTPException(
                status_code=404,
                detail="Incorrect email or password.")

        elif not await self.is_active(user):
            raise HTTPException(status_code=400,
                                detail="Inactive user")

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                data={"user_id": user.id},
                expires_delta=access_token_expires),
            "token_type": "bearer"}

    async def delete_user(
            self,
            user_id: int
    ) -> bool:
        return await self._delete(
            field=self.model.id,
            model_id=user_id)

    async def update_user(
            self,
            user_id: int,
            data: UserUpdate
    ):
        data = data.__dict__
        return await self._update(
            field=self.model.id,
            value=user_id,
            data=data
        )

    async def password_change(
            self,
            user_id: int,
            new_password: str
    ) -> UserInDB:
        new_password_hash = get_password_hash(new_password)
        data = {"hashed_password": new_password_hash}
        return await self._update(
            field=self.model.id,
            value=user_id,
            data=data
        )

    async def activate_user(
            self,
            user_id: int
    ) -> bool:
        data = {'is_active': True}
        return await self._update(
            field=self.model.id,
            value=user_id,
            data=data
        )

    async def is_active(self,
                        user: UserInDB
                        ) -> bool:
        return user.is_active

    async def is_superuser(self,
                           user: UserInDB
                           ) -> bool:
        return user.is_superuser
