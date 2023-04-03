from sqlalchemy import Column, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship

from app.services.databases.models.base import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates="comments")
    products = relationship('Product', back_populates="comments")
