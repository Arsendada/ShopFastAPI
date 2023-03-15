from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.api.utils.security import get_current_active_user
from app.core.jwt import generate_new_token
from app.databases.schemas.user.user import UserCreate, UserInDB, UserUpdate
from app.databases.repositories.user.user import UserCrud
from app.tasks.tasks import task_send_new_account, test_celery_start

router = APIRouter()


@router.post('/create')
async def user_create(user: UserCreate,
                          crud: UserCrud = Depends()):
    result = await crud.create_user(user)
    token = generate_new_token(user.email)
    task_send_new_account.delay(
        email_to=user.email, username=user.username, token=token
    )
    return {'result': result,
            'message': 'Confirm your mail'}


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


@router.post("/test-celery/", status_code=201)
def test_celery(
        value: int
):
    test_celery_start.delay(value)
    return {"msg": f"{value}"}