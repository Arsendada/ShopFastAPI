from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.utils.security import get_current_active_user
from app.databases.repositories.user.login import LoginCrud
from app.databases.schemas.tokens.tokens import Token
from app.databases.schemas.user.user import User

router = APIRouter()


@router.post('/token')
async def login_access_token(crud: LoginCrud = Depends(),
                             form_data: OAuth2PasswordRequestForm = Depends()
                             ) -> Token:
    return await crud.authenticate(
        email=form_data.username,
        password=form_data.password)


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user.__dict__


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]