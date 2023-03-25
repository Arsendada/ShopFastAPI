from starlette.requests import Request
from fastapi import APIRouter


router = APIRouter()

@router.post('/cart_test')
def test(request: Request):
    cart = request.session.get('cart', {})
    return cart