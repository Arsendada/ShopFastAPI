from app.services.databases.models.order.order import Item
from app.services.databases.repositories.base import BaseCrud


class ItemCrud(BaseCrud):

    async def add_item(self,
                       name: str,
                       price: int,
                       quantity: int,
                       order_id: int,
                       product_id: int):

        new_item = Item(name=name,
                        price=price,
                        quantity=quantity,
                        order_id=order_id,
                        product_id=product_id)

        self.sess.add(new_item)
        await self.sess.commit()
        await self.sess.refresh(new_item)
        return True
