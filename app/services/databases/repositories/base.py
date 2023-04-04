from typing import Optional, List, TypeVar, Type, ClassVar, Any

from anyio import EndOfStream
from asyncpg import UniqueViolationError
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.core.session import get_session

Model = TypeVar("Model")


class BaseCrud:

    model: ClassVar[Type[Model]]

    def __init__(
            self,
            db: AsyncSession = Depends(get_session)
    ):
        self._session = db

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
        return result.all()

    async def _get_relation_detail_one(
            self,
            relation_field: Any,
            filter_field: Any,
            filter_value: Any
    ) -> Optional[List[Model]]:
        stmt = (
            select(self.model)
            .options(selectinload(relation_field))
            .filter(filter_field == filter_value)
        )
        result = await self._session.scalar(stmt)
        return result

    async def _get_relation_list(
            self,
            limit: int,
            offset: int,
            relation_field: Any,
            filter_field: Any = None,
            filter_value: Any = None,
    ) -> Optional[List[Model]]:
        if not (filter_field and filter_value):
            stmt = (
                select(self.model)
                .options(selectinload(relation_field))
                .offset(offset)
                .limit(limit)
            )
        else:
            stmt = (
                select(self.model)
                .options(selectinload(relation_field))
                .filter(filter_field == filter_value)
                .offset(offset)
                .limit(limit)
            )
        result = await self._session.scalars(stmt)
        return result.all()

    async def _delete(
            self,
            field: Any,
            model_id: int,
    ) -> bool:
        stmt = (
            delete(self.model)
            .where(field == model_id)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        if result.rowcount:
            return True
        return None

    async def _update(
            self,
            field: Any,
            value: Any,
            data: dict
    ) -> Model:
        stmt = (
            update(self.model)
            .where(field == value)
            .values(**data)
            .returning(self.model)
        )
        try:
            result = await self._session.scalar(stmt)
            await self._session.commit()
            await self._session.refresh(result)
            return result
        except UnmappedInstanceError:
            return None
        except IntegrityError:
            return None

    async def _create(
            self,
            data: dict
    ) -> Model:
        try:
            new_obj = self.model(**data)
            self._session.add(new_obj)
            await self._session.commit()
            await self._session.refresh(new_obj)
            return new_obj
        except UniqueViolationError:
            return None
        except IntegrityError:
            return None
        except UnmappedInstanceError:
            return None
