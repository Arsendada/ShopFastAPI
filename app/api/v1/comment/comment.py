from fastapi import APIRouter, Depends, Security, HTTPException

from app.services.databases.repositories.comment.comment import CommentCrud
from app.services.databases.schemas.comment.comment import CommentModel
from app.services.databases.schemas.user.user import UserInDB
from app.services.security.permissions import get_current_active_user, get_current_active_superuser

router = APIRouter()


@router.post('/create')
async def create_comment(
        data: CommentModel,
        user: UserInDB = Depends(get_current_active_user),
        crud: CommentCrud = Depends(),
):
    if user.is_active or user.is_superuser:
        result = await crud.add_comment(user_id=user.id, data=data)
        return result
    return {'message': 'User is not active or admin'}


@router.delete('/delete/{comment_id}')
async def delete_comment(
        comment_id: int,
        user: UserInDB = Depends(get_current_active_user),
        crud: CommentCrud = Depends()
):
    comment = await crud.detail_comment(comment_id=comment_id)
    if not comment:
        return {'messages': 'Comment does not exists'}
    if not (user.id == comment.user_id or user.is_superuser):
        return {'messages': 'The user does not have rights or is not an admin'}
    result = await crud.delete_comment(comment_id=comment_id)
    if result:
        return {'messages': "comment successfully deleted"}
    return {'messages': "category does not exist"}


@router.get('/get_list_comment', dependencies=[Depends(get_current_active_superuser)])
async def get_list_comment(
        offset: int = 0,
        limit: int = 10,
        crud: CommentCrud = Depends()
):
    result = await crud.get_list_comment(
        offset=offset,
        limit=limit
    )
    return result


@router.get('/get_user_comment')
async def get_user_comment(
        user_id: int,
        offset: int = 0,
        limit: int = 20,
        user: UserInDB = Depends(get_current_active_user),
        crud: CommentCrud = Depends()
):
    if not (user.id == user_id or user.is_superuser):
        return {'messages': 'The user does not have rights or is not an admin'}
    result = await crud.get_user_comment(
        offset=offset,
        limit=limit,
        value=user_id)
    return result
