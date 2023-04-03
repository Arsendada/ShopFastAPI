from pydantic import BaseModel
from app.services.databases.schemas.base import BaseInDB

class CategoryDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Laptop"
        }

class CategoryInDB(CategoryDTO, BaseInDB):
    pass