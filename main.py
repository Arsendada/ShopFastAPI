from fastapi import FastAPI

from app.api.endpoints import category, product, user, login

app = FastAPI()




app.include_router(category.router,
                   prefix='/category',
                   tags=['Category'])

app.include_router(product.router,
                   prefix='/product',
                   tags=['Product'])


app.include_router(user.router,
                   prefix='/user',
                   tags=['User'])

app.include_router(login.router,
                   prefix='/login',
                   tags=['Login'])