from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.databases.models.product.product import Category
from app.databases.repositories.base import BaseCrud
from app.databases.schemas.product.category import CategoryModel
from sqlalchemy import update, select, delete



class CategoryCrud(BaseCrud):

    async def add_category(self, req: CategoryModel):
        new_category = Category(**req.dict())
        self.sess.add(new_category)
        await self.sess.commit()
        await self.sess.refresh(new_category)
        return new_category

    async def get_all_category(self) -> list[Category]:
        all_category = select(Category)
        result = await self.sess.scalars(all_category)
        return result.all()

    async def delete_category(self, cat_id: int):
        category_db = await self.sess.get(Category, cat_id)
        if not category_db:
            return False
        await self.sess.delete(category_db)
        await self.sess.commit()
        return True

    async def get_category_by_id(self, cat_id: int):

        return await self.sess.get(Category, cat_id)

    async def update_category_by_id(self, cat_id: int,
                                    cat_model: CategoryModel):
        stmt = (update(Category).
                where(Category.id == cat_id).
                values(**cat_model.dict()).
                returning(Category))
        try:
            result = await self.sess.scalar(stmt)
            await self.sess.commit()
            await self.sess.refresh(result)
            return result
        except UnmappedInstanceError:
            return False