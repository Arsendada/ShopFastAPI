from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.services.databases.models.base import Base


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(60), index=True)
    email = Column(String(50), index=True, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    telephone = Column(String, nullable=False)

    items = relationship('Item', back_populates='order')


