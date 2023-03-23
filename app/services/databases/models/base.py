from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        default=datetime.now)
    updated_at = Column(DateTime(timezone=True),
                        nullable=False,
                        default=datetime.now,
                        onupdate=datetime.now)
