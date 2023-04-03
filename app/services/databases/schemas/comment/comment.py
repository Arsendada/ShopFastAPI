from pydantic import BaseModel
from app.services.databases.schemas.base import BaseInDB

class CommentDTO(BaseModel):
    text: str
    product_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "text": "thr best comment",
            "product_id": 1,
        }


class CommentInDB(CommentDTO, BaseInDB):
    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "created_at": "2023-04-02 22:03:21.605901 +00:00",
            "updated_at": "2023-04-02 22:03:21.605901 +00:00",
            "text": "thr best comment",
            "product_id": 1,
        }