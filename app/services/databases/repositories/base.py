from typing import Optional, List, TypeVar, Type, ClassVar, Any
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.core.session import get_session

Model = TypeVar("Model")


class BaseCrud:
    model: ClassVar[Type[Model]]

    def __init__(self, db: AsyncSession = Depends(get_session)):
        self._session = db

    @classmethod
    async def _check_unique(
            cls,
            result,
            unique: bool = False
    ) -> Optional[List[Model]]:
        if unique:
            return result.unique().all()
        return result.all()

    async def _get(
            self,
            field: Any,
            value: Any,
    ) -> Optional[Model]:

        stmt = (
            select(self.model)
            .where(field == value)
        )

        result = await self._session.scalar(stmt)
        return result

    async def _get_list(
            self,
            limit: int,
            offset: int,
            field: Any = None,
            value: Any = None,
            unique: bool = False
    ) -> Optional[List[Model]]:

        if field and value:
            stmt = (
                select(self.model)
                .where(field == value)
                .offset(offset)
                .limit(limit)
            )
        else:
            stmt = (
                select(self.model)
                .offset(offset)
                .limit(limit)
            )
        result = await self._session.scalars(stmt)
        return await self._check_unique(
            result=result,
            unique=unique
        )

    async def _delete(
            self,
            field: Any,
            model_id: int,
    ) -> bool:
        model_db = await self._get(
            field=field,
            value=model_id
        )
        if not model_db:
            return False
        await self._session.delete(model_db)
        await self._session.commit()
        return True

    async def _update(
            self,
            field: Any,
            value: Any,
            data: Model
    ) -> Model:
        stmt = (
            update(self.model).
            where(field == value).
            values(**data.dict()).
            returning(self.model)
        )
        try:
            result = await self._session.scalar(stmt)
            await self._session.commit()
            await self._session.refresh(result)
            return result
        except UnmappedInstanceError:
            return False
        except IntegrityError:
            return False
