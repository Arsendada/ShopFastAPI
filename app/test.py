bla = {}
bla.setdefault('cart', {})
set_data = {2: {'quantity': 0,
                                     'price': str(1),
                                     'name': 1}}
bla['cart'].setdefault(2, set_data)
print(bla)