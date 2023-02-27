from pydantic import BaseModel


class CategoryModel(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Laptop"
        }

