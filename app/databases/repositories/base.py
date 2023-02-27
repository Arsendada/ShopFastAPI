from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.session import get_session


class BaseCrud:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.sess = db
