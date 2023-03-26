from starlette.requests import Request
from decimal import Decimal

from app.services.databases.models.product.product import Product


class Cart:
    def __init__(self, request: Request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = {}
            request.session['cart'] = cart
        self.cart = cart

    def add_to_cart(
            self,
            request: Request,
            product: Product,
            quantity: int,
            update_quantity=False,
    ) -> bool:
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'name': product.name}
            request.session['cart']['product_id'] = self.cart[product_id]
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            request.session['cart'][product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            request.session['cart'][product_id]['quantity'] += quantity
        return self.cart[product_id]
