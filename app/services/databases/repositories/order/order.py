from app.services.databases.models.order.order import Order
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.schemas.order.order import OrderModel


class OrderCrud(BaseCrud):

    async def add_order(self,
                        data: OrderModel):

        new_order = Order(**data.dict())
        self.sess.add(new_order)
        await self.sess.commit()
        await self.sess.refresh(new_order)
        return new_order