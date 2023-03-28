from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.services.cart.cart import Cart
from app.services.databases.repositories.order.item import ItemCrud
from app.services.databases.repositories.order.order import OrderCrud
from app.services.databases.schemas.order.order import OrderModel


router = APIRouter()


@router.post('add_order')
async def add_order(
        request: Request,
        order: OrderModel,
        order_crud: OrderCrud = Depends(),
        item_crud: ItemCrud = Depends(),
):
    pass