from sqlalchemy import Column, VARCHAR, ForeignKey, Text, Boolean, DECIMAL, Integer
from sqlalchemy.orm import relationship

from app.services.databases.models.base import Base



class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), unique=True, index=True)
    category_id = Column(Integer, ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    available = Column(Boolean, default=True)
    description = Column(Text, default=None, nullable=True)

    category = relationship('Category', back_populates="products")
    comments = relationship('Comment', back_populates="products")

