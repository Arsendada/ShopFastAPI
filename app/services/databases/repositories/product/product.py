from sqlalchemy.orm.exc import UnmappedInstanceError

from app.services.databases.models.product.product import Product, Category
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.schemas.product.product import ProductModel
from sqlalchemy import update, select


class ProductCrud(BaseCrud):

    model = Product

    async def add_product(
            self,
            data: ProductModel
    ):
        return await self._create(data=data.__dict__)

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

    async def delete_product(
            self,
            product_id: int
    ) -> bool:

        return await self._delete(
            field=self.model.id,
            model_id=product_id)

    async def update_product(self,
                             product_id: int,
                             data: ProductModel) -> bool:
        data = data.__dict__
        return await self._update(
            field=self.model.id,
            value=product_id,
            data=data
        )
