from sqlalchemy import select

from app.services.databases.models.product.product import Comment
from app.services.databases.repositories.base import BaseCrud
from app.services.databases.schemas.comment.comment import CommentModel


class CommentCrud(BaseCrud):

    model = Comment

    async def add_comment(
            self,
            user_id: str,
            data: CommentModel
    ):
        new_comment = Comment(**data.dict(), user_id=user_id)
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        return new_comment

    async def delete_comment(
            self,
            comment_id: int
    ):
        result = await self._get(model_id=comment_id)
        if not result:
            return False
        await self.session.delete(result)
        await self.session.commit()
        return True


    async def get_by_user_id(
            self,
            user_id: int
    ):
        stmt = (
            select(Comment).
            where(Comment.user_id == user_id)
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def get_list_comment(
            self,
            offset: int = 0,
            limit: int = 20
    ):
        stmt = (
            select(Comment).
            offset(offset).
            limit(limit)
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def get_comment_by_id(
            self,
            comment_id: int
    ):
        return await self._get(model_id=comment_id)
