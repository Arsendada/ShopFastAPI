from pydantic import BaseModel, EmailStr


class OrderModel(BaseModel):
    full_name: str
    email: EmailStr
    address: str
    city: str
    country: str
    telephone: str
