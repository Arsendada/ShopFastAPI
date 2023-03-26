from starlette.requests import Request
from decimal import Decimal

from app.services.databases.models.product.product import Product


class Cart:
    def __init__(self, request: Request):
        request.session.get('cart', {})

    def add_to_cart(
            self,
            request: Request,
            product: Product,
            quantity: int,
            update_quantity=False,
    ) -> bool:

        product_id = str(product.id)
        if product_id not in request.session['cart']:
            set_data = {product_id: {'quantity': 0,
                                     'price': str(product.price),
                                     'name': product.name}}
            request.session.setdefault('cart', set_data)
        if update_quantity:
            request.session['cart'][product_id]['quantity'] = quantity
        else:
            request.session['cart'][product_id]['quantity'] += quantity
        return True
