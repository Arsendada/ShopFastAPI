from pydantic import BaseModel, condecimal


class CommentModel(BaseModel):
    text: str
    product_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "text": "thr best comment",

        }