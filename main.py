from fastapi import FastAPI

from app.api.endpoints import category, product


app = FastAPI()




app.include_router(category.router,
                   prefix='/category',
                   tags=['Category'])

app.include_router(product.router,
                   prefix='/product',
                   tags=['Product'])
