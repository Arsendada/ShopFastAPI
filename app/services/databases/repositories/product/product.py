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
        self._session.add(new_product)
        await self._session.commit()
        await self._session.refresh(new_product)
        return new_product

    async def get_detail_product(
            self,
            product_id: int,
    ):
        result = await self._get(
            field=self.model.id,
            value=product_id
        )

        if result:
            return result

        return {'message': 'Product does not exist'}

    async def get_list(
            self,
            offset: int = 0,
            limit: int = 20,
            category_id: int = None
):
        if category_id:
            return await self._get_list(
                limit=limit,
                offset=offset,
                field=self.model.category_id,
                value=category_id
            )
        return await self._get_list(
            limit=limit,
            offset=offset
        )

    async def delete_product(self,
                             product_id: int
                             ) -> bool:
        product_db = await self._get(model_id=product_id)
        if not product_db:
            return False
        await self._session.delete(product_db)
        await self._session.commit()
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
            result = await self._session.scalar(stmt)
            await self._session.commit()
            await self._session.refresh(result)
            return result
        except UnmappedInstanceError:
            return False