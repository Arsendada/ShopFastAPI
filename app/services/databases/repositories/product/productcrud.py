from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.databases.models.product.product import Product, Category
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.schemas.product.product import ProductModel
from sqlalchemy import update, select


class ProductCrud(BaseCrud):

    model = Product

    async def add_product(self,
                          data: ProductModel
                          ):
        category_id = await self._get(model_email=data.category_id)

        if not category_id:
            return f'Missing category with id {data.category_id}'
        new_product = Product(**data.dict())
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product

    async def get_product(self,
                          product_id
                          ):
        result = await self._get(model_id=product_id)

        if result:
            return result

        return {'message': 'Product does not exist'}

    async def get_all_product(self,
                              offset: int = 0,
                              limit: int = 20
                              ):
        stmt = (
            select(Product).
            offset(offset).
            limit(limit)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_all_product_by_category(
            self,
            category_id: int,
            offset: int = 0,
            limit: int = 20
    ):
        stmt = (
            select(Product).
            where(Product.category_id == category_id).
            offset(offset).
            limit(limit)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def delete_product(self,
                             product_id: int
                             ) -> bool:
        product_db = await self._get(model_id=product_id)
        if not product_db:
            return False
        await self.session.delete(product_db)
        await self.session.commit()
        return True

    async def update_product(self,
                             product_id: int,
                             data: ProductModel) -> bool:
        stmt = (
            update(Product).
            where(Product.id == product_id).
            values(**data.dict()).
            returning(Product)
        )

        try:
            result = await self.session.scalar(stmt)
            await self.session.commit()
            await self.session.refresh(result)
            return result
        except UnmappedInstanceError:
            return False
