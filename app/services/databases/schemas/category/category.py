from pydantic import BaseModel
from app.services.databases.schemas.base import BaseInDB

class CategoryDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Laptop"
        }

class CategoryInDB(
    CategoryDTO,
    BaseInDB
):
    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "created_at": "2023-04-02 22:03:21.605901 +00:00",
            "updated_at": "2023-04-02 22:03:21.605901 +00:00",
            "name": "Laptop",
        }