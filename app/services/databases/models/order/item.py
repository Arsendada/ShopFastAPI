from sqlalchemy import Column, VARCHAR, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship

from app.services.databases.models.base import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    price = Column(Numeric(precision=8))
    quantity = Column(Integer)

    order_id = Column(Integer, ForeignKey('order.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=False)

    order = relationship('Order', back_populates="items")