import datetime
from sqlalchemy import Boolean, Integer
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.databases.models.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    comments = relationship('Comment', back_populates="user", lazy=True)
