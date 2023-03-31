from fastapi import APIRouter, Depends

from app.services.security.permissions import get_current_active_user, get_current_active_superuser
from app.services.security.jwt import generate_new_token
from app.services.databases.schemas.user.user import UserCreate, UserInDB, UserUpdate
from app.services.databases.repositories.user.user import UserCrud
from app.services.tasks.tasks import task_send_new_account


router = APIRouter()


@router.post('/create')
async def user_create(
        user: UserCreate,
        crud: UserCrud = Depends()
):
    result = await crud.create_user(user)
    token = generate_new_token(user.email)
    task_send_new_account.delay(
        email_to=user.email,
        username=user.username,
        token=token
    )
    return {'result': result,
            'message': 'Confirm your mail'}


@router.put('/update/{user_id}')
async def update_user(
        user_id: int,
        data: UserUpdate,
        current_user: UserInDB = Depends(get_current_active_user),
        crud: UserCrud = Depends()
):
    if not (current_user.id == user_id or current_user.is_superuser):
        return {'messages': 'The user does not have rights or is not an admin'}
    result = await crud.update_user(user_id,
                                    data)
    return result


@router.delete('/delete/{user_id}')
async def delete_user(
        user_id: int,
        current_user: UserInDB = Depends(get_current_active_user),
        crud: UserCrud = Depends()
) -> bool:
    if not (current_user.id == user_id or current_user.is_superuser):
        return {'messages': 'The user does not have rights or is not an admin'}
    result = await crud.delete_user(user_id)
    return result


@router.get('/list', dependencies=[Depends(get_current_active_superuser)])
async def get_list_user(
        offset: int = 0,
        limit: int = 10,
        crud: UserCrud = Depends()):

    result = await crud.get_list_user(
        offset=offset,
        limit=limit
    )
    return result
