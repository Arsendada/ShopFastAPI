from pydantic import BaseModel
from app.services.databases.schemas.base import BaseInDB

class ItemDTO(BaseInDB):
    name: str
    price: int
    quantity: int
    order_id: int
    product_id: int
