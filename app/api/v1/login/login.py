from typing import Dict, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.services.security.permissions import get_current_active_user
from app.services.security.jwt import generate_new_token, verify_new_token
from app.services.databases.repositories.user.user import UserCrud
from app.services.databases.schemas.tokens.tokens import Token
from app.services.databases.schemas.user.user import (UserPasswordDTO,
                                                      UserInDB)
from app.services.tasks.tasks import task_send_password_reset

router = APIRouter()


@router.post('/token')
async def login_access_token(
        crud: UserCrud = Depends(),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    return await crud.authenticate(
        email=form_data.username,
        password=form_data.password)


@router.get("/users/me/", response_model=UserInDB)
async def read_users_me(
        current_user: UserInDB = Depends(get_current_active_user)
) -> UserInDB:
    return current_user.__dict__


@router.post("/password-recovery/{email}")
async def recover_password(
        email: str,
        crud: UserCrud = Depends()
) -> Dict[str, str]:
    user = await crud.get(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_new_token(email=email)
    task_send_password_reset.delay(
        email_to=user.email,
        username=user.username,
        token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/password/change/{token}")
async def password_change(
        new_password: UserPasswordDTO,
        token: str,
        crud: UserCrud = Depends()
) -> UserInDB:
    email = verify_new_token(token).get('email')

    if not email:
        raise HTTPException(status_code=400,
                            detail="Invalid token")
    user = await crud.get(email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400,
                            detail="Inactive user")
    result = await crud.password_change(
        user_id=user.id,
        new_password=new_password.password
    )
    return result


@router.get('/register/{token}')
async def activate_user(
        token: str,
        crud: UserCrud = Depends()
) -> Dict[str, Union[bool, str]]:
    email = verify_new_token(token).get('email')
    user = await crud.get(email=email)
    if user:
        await crud.activate_user(user_id=user.id)
        return {"success": True,
                'detail': f'User {user.username} has registered by email: {user.email} '}
    raise HTTPException(404, 'Registration time expired')
