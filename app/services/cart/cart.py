from typing import Dict, Any, Union

from starlette.requests import Request
from decimal import Decimal

from app.services.databases.models.product.product import Product


class Cart:
    def __init__(
            self,
            request: Request
    ):
        request.session.setdefault('cart', {})
        self.cart = request.session['cart']

    def add_to_cart(
            self,
            request: Request,
            product: Product,
            quantity: int,
            update_quantity=False,
    ) -> Dict[str, Dict[str, Union[str, int]]]:

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
        self.cart = request.session['cart']
        return self.cart

    def remove(
            self,
            request: Request,
            product_id: str
    ) -> Dict[str, str]:

        if product_id in self.cart:
            del request.session['cart'][product_id]
            return {'message': 'successfully'}
        return None

    def get_cart(
            self
    ) -> Dict[str, Union[int, Dict[str, Dict[str, Union[str, int]]]]]:
        quantity = len(self.cart)
        return {'quantity': quantity, "cart": self.cart}

    def clear(
            self,
            request: Request
    ) -> None:
        del request.session['cart']

    def get_total_price(self) -> int:
        return sum(Decimal(item['price'])*item['quantity']
                   for item in self.cart.values())
