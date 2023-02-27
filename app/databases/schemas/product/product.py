from pydantic import BaseModel, condecimal


class ProductModel(BaseModel):
    name: str
    category_id: int
    price: condecimal(max_digits=10, decimal_places=2)
    available: bool = True
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Laptop 3000",
            "category_id": "2",
            "price": "178.12",
            "available": "True",
            "description": "Loren ipsum",
        }
