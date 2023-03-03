from fastapi import APIRouter, Depends, HTTPException

from app.api.utils.security import get_current_active_user
from app.databases.schemas.user.user import UserCreate, UserInDB, UserUpdate
from app.databases.repositories.user.user import UserCrud


router = APIRouter()


@router.post('/create')
async def user_create(req: UserCreate,
                          crud: UserCrud = Depends()):
    result = await crud.create_user(req)
    return result


@router.put('/update/{user_id}')
async def update_user(user_id: int,
                      data: UserUpdate,
                      current_user: UserInDB = Depends(get_current_active_user),
                      crud: UserCrud = Depends()):
    if current_user.id != user_id:
        return False
    result = await crud.update_user(user_id, data)
    return result


@router.delete('/delete/{user_id}')
async def delete_user(user_id: int,
                         current_user: UserInDB = Depends(get_current_active_user),
                         crud: UserCrud = Depends()) -> bool:
    if current_user.id != user_id:
        return False
    result = await crud.delete_user(user_id)
    return result