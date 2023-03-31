from sqlalchemy import select

from app.services.databases.models.order.order import Order
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.schemas.order.order import OrderModel


class OrderCrud(BaseCrud):

    model = Order

    async def add_order(
            self,
            data: OrderModel
    ):

        new_order = Order(**data.dict())
        self._session.add(new_order)
        await self._session.commit()
        await self._session.refresh(new_order)
        return new_order

    async def get_detail_order(
            self,
            order_id: int
    ):
        return await self._get(
            field=self.model.id,
            value=order_id,
        )

    async def list_order(
            self,
            offset: int = 0,
            limit: int = 20
    ):
        return await self._get_list(
            offset=offset,
            limit=limit,
            unique=True
        )

    async def get_user_order(
            self,
            value: str,
            offset: int,
            limit: int
    ):
        return await self._get_list(
            offset=offset,
            limit=limit,
            field=self.model.email,
            value=value,
            unique=True
        )
