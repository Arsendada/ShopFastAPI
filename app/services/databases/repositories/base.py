import typing

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.session import get_session


Model = typing.TypeVar("Model")


class BaseCrud:

    model: typing.ClassVar[typing.Type[Model]]

    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.session = db

    async def _get(
            self,
            model_id: int = None,
            model_email: str = None,
    ) -> typing.Optional[Model]:

        if model_id:
            return await self.session.get(self.model, model_id)

        if model_email:
            stmt = (
                select(self.model)
                .where(self.model.email == model_email)
            )
            result = await self.session.scalar(stmt)
            return result

