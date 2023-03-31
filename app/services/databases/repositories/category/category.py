from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.databases.models.product.product import Category
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.schemas.category.category import CategoryModel
from sqlalchemy import update, select


class CategoryCrud(BaseCrud):

    model = Category

    async def add_category(
            self,
            req: CategoryModel
    ):
        new_category = Category(**req.dict())
        self._session.add(new_category)
        await self._session.commit()
        await self._session.refresh(new_category)
        return new_category

    async def get_list(
            self,
            limit: int,
            offset: int,
    ):

        return await self._get_list(
            limit=limit,
            offset=offset
        )

    async def delete_category(
            self,
            category_id: int
    ):
        category_db = await self._get(model_id=category_id)
        if not category_db:
            return False
        await self._session.delete(category_db)
        await self._session.commit()
        return True

    async def detail_category(
            self,
            category_id: int
    ):

        return await self._get(
            field=self.model.id,
            value=category_id,
        )

    async def update_category_by_id(
            self,
            cat_id: int,
            data: CategoryModel
    ):
        stmt = (
            update(Category).
            where(Category.id == cat_id).
            values(**data.dict()).
            returning(Category)
        )
        try:
            result = await self._session.scalar(stmt)
            await self._session.commit()
            await self._session.refresh(result)
            return result
        except UnmappedInstanceError:
            return False
