from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.services.cart.cart import Cart
from app.services.databases.repositories.order.item import ItemCrud
from app.services.databases.repositories.order.order import OrderCrud
from app.services.databases.schemas.order.order import OrderModel
from app.services.security.permissions import get_current_active_superuser, get_current_active_user


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


@router.get('/get_order/{order_id}', dependencies=[Depends(get_current_active_superuser)])
async def get_order(
        order_id: int,
        order_crud: OrderCrud = Depends()
):
    order = await order_crud.get_detail_order(order_id)
    if order:
        return order
    return {'message': 'order does not exist'}


@router.get('/list', dependencies=[Depends(get_current_active_superuser)])
async def get_list_order(
        offset: int = 0,
        limit: int = 10,
        order_crud: OrderCrud = Depends()
):
    result = await order_crud.list_order(
        offset=offset,
        limit=limit)
    return result


@router.get('/user_order', dependencies=[Depends(get_current_active_superuser)])
async def get_user_order(
        email: str,
        offset: int = 0,
        limit: int = 10,
        order_crud: OrderCrud = Depends()
):
    result = await order_crud.get_user_order(
        value=email,
        offset=offset,
        limit=limit
    )
    return result
