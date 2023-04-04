from typing import List

from pydantic import BaseModel, EmailStr
from app.services.databases.schemas.base import BaseInDB
from app.services.databases.schemas.order.item import ItemInDB


class OrderDTO(BaseModel):
    full_name: str
    email: EmailStr
    address: str
    city: str
    country: str
    telephone: str

    class Config:
        orm_mode = True
        schema_extra = {
            "full_name": "Arsen",
            "email": "user_example@gmail.com",
            "address": 'Country, City, Street, house number',
            "country": "Russia",
            "telephone": "88002003040",
        }

class OrderInDB(BaseInDB, OrderDTO):

    items: list[ItemInDB]
    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "created_at": "2023-04-02 22:03:21.605901 +00:00",
            "updated_at": "2023-04-02 22:03:21.605901 +00:00",
            "full_name": "Arsen",
            "email": "user_example@gmail.com",
            "address": 'Country, City, Street, house number',
            "country": "Russia",
            "telephone": "88002003040",
        }
