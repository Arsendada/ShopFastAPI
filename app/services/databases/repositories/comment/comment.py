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
        self._session.add(new_comment)
        await self._session.commit()
        await self._session.refresh(new_comment)
        return new_comment

    async def delete_comment(
            self,
            comment_id: int
    ):
        result = await self._get(model_id=comment_id)
        if not result:
            return False
        await self._session.delete(result)
        await self._session.commit()
        return True


    async def get_user_comment(
            self,
            offset: int,
            limit: int,
            value: int

    ):
        return await self._get_list(
            offset=offset,
            limit=limit,
            field=self.model.user_id,
            value=value,
            unique=True
        )

    async def get_list_comment(
            self,
            offset: int = 0,
            limit: int = 20
    ):
        return await self._get_list(
            offset=offset,
            limit=limit,
            unique=True
        )
