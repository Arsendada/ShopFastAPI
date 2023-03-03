from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.utils.security import get_current_active_user
from app.core.email import send_reset_password_email
from app.core.jwt import generate_password_reset_token
from app.databases.repositories.user.user import UserCrud
from app.databases.schemas.tokens.tokens import Token
from app.databases.schemas.user.user import UserInDB

router = APIRouter()


@router.post('/token')
async def login_access_token(crud: UserCrud = Depends(),
                             form_data: OAuth2PasswordRequestForm = Depends()
                             ) -> Token:
    return await crud.authenticate(
        email=form_data.username,
        password=form_data.password)


@router.get("/users/me/", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user.__dict__


@router.get("/users/me/items/")
async def read_own_items(current_user: UserInDB = Depends(get_current_active_user)) -> str:
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/password-recovery/{email}")
async def recover_password(email: str,
                           crud: UserCrud = Depends()):
    user = await crud.get_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, username=user.username, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


