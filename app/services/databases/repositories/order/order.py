from app.services.databases.models.order.order import Order
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.schemas.order.order import OrderModel


class OrderCrud(BaseCrud):

    model = Order

    async def add_order(
            self,
            data: OrderModel
    ):

        return await self._create(data=data.__dict__)

    async def get_detail_order(
            self,
            order_id: int
    ):
        return await self._get_relation_detail_one(
            relation_field=self.model.items,
            filter_field=self.model.id,
            filter_value=order_id
        )

    async def list_order(
            self,
            offset: int = 0,
            limit: int = 20
    ):
        return await self._get_relation_list(
            offset=offset,
            limit=limit,
            relation_field=self.model.items
        )

    async def get_user_order(
            self,
            value: str,
            offset: int,
            limit: int
    ):
        return await self._get_relation_list(
            offset=offset,
            limit=limit,
            filter_field=self.model.email,
            filter_value=value,
            relation_field=self.model.items
        )
