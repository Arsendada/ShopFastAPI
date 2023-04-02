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
        new_comment = data.__dict__
        new_comment["user_id"] = user_id
        return await self._create(data=new_comment)

    async def delete_comment(
            self,
            comment_id: int
    ):
        return await self._delete(
            field=self.model.id,
            value=comment_id
        )


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

    async def detail_comment(
            self,
            comment_id: int
    ):
        return await self._get(
            field=self.model.id,
            value=comment_id
        )
