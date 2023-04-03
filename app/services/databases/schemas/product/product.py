from pydantic import BaseModel, condecimal
from app.services.databases.schemas.base import BaseInDB


class ProductUpdateDTO(BaseModel):
    name: str
    category_id: int
    price: condecimal(max_digits=10, decimal_places=2)
    available: bool = True
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Laptop 3000",
            "price": "178.12",
            "available": "True",
            "description": "Loren ipsum",
        }


class ProductCreateDTO(ProductUpdateDTO):
    category_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Laptop 3000",
            "category_id": "2",
            "price": "178.12",
            "available": "True",
            "description": "Loren ipsum",
        }


class ProductInDB(BaseInDB, ProductCreateDTO):
    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "created_at": "2023-04-02 22:03:21.605901 +00:00",
            "updated_at": "2023-04-02 22:03:21.605901 +00:00",
            "name": "Laptop 3000",
            "category_id": "2",
            "price": "178.12",
            "available": "True",
            "description": "Loren ipsum",
        }
