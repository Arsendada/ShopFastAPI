from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.services.cart.cart import Cart
from app.services.databases.repositories.order.item import ItemCrud
from app.services.databases.repositories.order.order import OrderCrud
from app.services.databases.schemas.order.order import OrderModel


router = APIRouter()


@router.post('/create')
async def add_order(
        request: Request,
        order: OrderModel,
        order_crud: OrderCrud = Depends(),
        item_crud: ItemCrud = Depends(),
):
    cart = Cart(request)
    values = cart.cart
    if len(values) < 1:
        return {'detail': 'There are no products in the cart'}

    total_price = cart.get_total_price()
    order_obj = await order_crud.add_order(order)

    for product in values:
        await item_crud.add_item(name=values[product]['name'],
                                 price=values[product]['price'],
                                 quantity=values[product]['quantity'],
                                 order_id=order_obj.id,
                                 product_id=int(product))
    result_order = await order_crud.get_detail_order(order_obj.id)
    cart.clear(request)

    return {'total_price': total_price, 'order': result_order}

