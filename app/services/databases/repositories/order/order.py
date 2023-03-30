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
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order

    async def get_detail_order(
            self,
            order_id: int
    ):
        return await self._get(model_id=order_id)

    async def get_list_order(
            self,
            offset: int = 0,
            limit: int = 20
    ):
        stmt = (
            select(Order).
            offset(offset).
            limit(limit)
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def get_by_email(
            self,
            email: str
    ):
        stmt = (select(Order).where(Order.email == email))
        result = await self.session.scalars(stmt)
        return result.unique().all()
