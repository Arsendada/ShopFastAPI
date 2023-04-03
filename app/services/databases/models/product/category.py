from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.orm import relationship

from app.services.databases.models.base import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), unique=True, index=True)

    products = relationship('Product', back_populates="category")
