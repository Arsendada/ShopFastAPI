from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException
import random
from app.services.databases.repositories.product.productcrud import ProductCrud
from app.services.cart.cart import Cart

router = APIRouter()

@router.post('/cart_add')
async def cart_add(
        request: Request,
        product_id: int,
        quantity: int = 1,
        update_quantity: bool = False,
        crud: ProductCrud = Depends(),
):
    try:
        cart = Cart(request)
        product = await crud.get_product(product_id)
        cart.add_to_cart(request=request,
                         product=product,
                         quantity=quantity,
                         update_quantity=update_quantity)
        return request.session
    except AttributeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={product_id}"
        )