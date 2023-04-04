from typing import Dict, Union, Optional

from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException
from app.services.databases.repositories.product.product import ProductCrud
from app.services.cart.cart import Cart

router = APIRouter()

@router.post('/cart_add')
async def cart_add(
        request: Request,
        product_id: int,
        quantity: int = 1,
        update_quantity: bool = False,
        crud: ProductCrud = Depends(),
) -> Dict[str, Dict[str, Union[str, int]]]:
    try:
        cart = Cart(request)
        product = await crud.get_detail_product(product_id=product_id)
        result = cart.add_to_cart(
            request=request,
            product=product,
            quantity=quantity,
            update_quantity=update_quantity
        )
        return result
    except AttributeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={product_id}"
        )


@router.delete('/delete')
async def cart_delete(
        product_id: str,
        request: Request
) -> Optional[Dict[str, str]]:
    cart = Cart(request)
    result = cart.remove(request=request,
                         product_id=product_id)
    if result:
        return result
    raise HTTPException(404, 'Product not in cart')


@router.get('/get')
async def cart_get(
        request: Request
) -> Dict[str, Union[int, Dict[str, Dict[str, Union[str, int]]]]]:
    cart = Cart(request)
    result = cart.get_cart()
    return result
