from fastapi import APIRouter

from app.api.v1 import category, product, user, login


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