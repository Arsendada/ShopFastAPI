from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.services.databases.repositories.comment.comment import CommentCrud
from app.services.databases.schemas.comment.comment import CommentDTO, CommentInDB
from app.services.databases.schemas.user.user import UserInDB
from app.services.security.permissions import get_current_active_user, get_current_active_superuser

router = APIRouter()


@router.post('/create')
async def create_comment(
        data: CommentDTO,
        user: UserInDB = Depends(get_current_active_user),
        crud: CommentCrud = Depends(),
) -> CommentInDB:
    if not (user.is_active or user.is_superuser):
        raise HTTPException(404, 'User is not active or admin')
    result = await crud.add_comment(
        user_id=user.id,
        data=data
    )
    if result:
        return result
    raise HTTPException(404, 'Product id does not exists')



@router.delete('/delete/{comment_id}')
async def delete_comment(
        comment_id: int,
        user: UserInDB = Depends(get_current_active_user),
        crud: CommentCrud = Depends()
) -> Dict[str, str]:
    comment = await crud.detail_comment(comment_id=comment_id)
    if not comment:
        raise HTTPException(404, 'Comment does not exists')
    if not (user.id == comment.user_id or user.is_superuser):
        raise HTTPException(404, 'The user does not have rights or is not an admin')
    result = await crud.delete_comment(comment_id=comment_id)
    if result:
        return {'messages': "comment successfully deleted"}
    raise HTTPException(404, "category does not exist")


@router.get('/get_list_comment', dependencies=[Depends(get_current_active_superuser)])
async def get_list_comment(
        offset: int = 0,
        limit: int = 10,
        crud: CommentCrud = Depends()
) -> List[Optional[CommentInDB]]:
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
) -> List[Optional[CommentInDB]]:
    if not (user.id == user_id or user.is_superuser):
        raise HTTPException(404, 'The user does not have rights or is not an admin')
    result = await crud.get_user_comment(
        offset=offset,
        limit=limit,
        value=user_id)
    return result
