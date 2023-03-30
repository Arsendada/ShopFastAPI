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
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category

    async def get_all_category(self) -> list[Category]:
        all_category = select(Category)
        result = await self.session.scalars(all_category)
        return result.all()

    async def delete_category(
            self,
            category_id: int
    ):
        category_db = await self._get(model_id=category_id)
        if not category_db:
            return False
        await self.session.delete(category_db)
        await self.session.commit()
        return True

    async def get_category_by_id(
            self,
            cat_id: int
    ):

        return await self._get(model_id=cat_id)

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
            result = await self.session.scalar(stmt)
            await self.session.commit()
            await self.session.refresh(result)
            return result
        except UnmappedInstanceError:
            return False
