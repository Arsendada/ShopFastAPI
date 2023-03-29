from fastapi import APIRouter

from app.api.v1.category import category
from app.api.v1.product import product
from app.api.v1.user import user
from app.api.v1.login import login
from app.api.v1 import test_celery
from app.api.v1.cart import cart
from app.api.v1.order import order
from app.api.v1.comment import comment


router = APIRouter()


router.include_router(category.router,
                      prefix='/category',
                      tags=['Category'])

router.include_router(product.router,
                      prefix='/product',
                      tags=['Product'])

router.include_router(user.router,
                      prefix='/user',
                      tags=['User'])

router.include_router(login.router,
                      tags=['Login'])

router.include_router(test_celery.router,
                      tags=['Test_celery'])

router.include_router(cart.router,
                      prefix='/cart',
                      tags=['Cart'])

router.include_router(order.router,
                      prefix='/order',
                      tags=['Order'])

router.include_router(comment.router,
                      prefix='/comment',
                      tags=['Comment'])