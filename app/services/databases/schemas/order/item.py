from app.services.databases.schemas.base import BaseInDB

class ItemInDB(BaseInDB):
    name: str
    price: int
    quantity: int
    order_id: int
    product_id: int
    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "created_at": "2023-04-02 22:03:21.605901 +00:00",
            "updated_at": "2023-04-02 22:03:21.605901 +00:00",
            "name": "Laptop",
            "price": 12312,
            "quantity": 3,
            'order_id': 5,
            "product_id": 7,
        }
