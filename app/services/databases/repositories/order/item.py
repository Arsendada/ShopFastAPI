from app.services.databases.models.order.order import Item
from app.services.databases.repositories.base import BaseCrud


class ItemCrud(BaseCrud):
    model = Item

    async def add_item(
            self,
            name: str,
            price: int,
            quantity: int,
            order_id: int,
            product_id: int
    ):

        new_item = dict(
            name=name,
            price=price,
            quantity=quantity,
            order_id=order_id,
            product_id=product_id
        )

        return await self._create(data=new_item)
