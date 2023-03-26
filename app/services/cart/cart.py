from starlette.requests import Request
from decimal import Decimal

from app.services.databases.models.product.product import Product


class Cart:
    def __init__(self, request: Request) -> None:
        request.session.setdefault('cart', {})
        self.cart = request.session['cart']

    def add_to_cart(
            self,
            request: Request,
            product: Product,
            quantity: int,
            update_quantity=False,
    ) -> bool:

        product_id = str(product.id)
        if product_id not in request.session['cart']:
            set_data = {'quantity': 0,
                        'price': str(product.price),
                        'name': product.name}
            request.session['cart'].setdefault(product_id, set_data)
        if update_quantity:
            request.session['cart'][product_id]['quantity'] = quantity
        else:
            request.session['cart'][product_id]['quantity'] += quantity
        return True

    def remove(
            self,
            request: Request,
            product_id: str
    ) -> bool:

        if product_id in self.cart:
            del request.session['cart'][product_id]
            return {'message': 'successfully'}
        return {'message': 'Product not in cart'}

    def get_cart(self):
        quantity = len(self.cart)
        return {'quantity': quantity, "cart": self.cart}

    def clear(self, request: Request):
        del request.session['cart']
