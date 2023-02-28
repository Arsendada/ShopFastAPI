from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.databases.repositories.user.login import LoginCrud
from app.databases.schemas.tokens.tokens import Token

router = APIRouter()


@router.post('/access-token')
async def login_access_token(crud: LoginCrud = Depends(),
                             form_data: OAuth2PasswordRequestForm = Depends()
                             ) -> Token:
    return await crud.authenticate(
        email=form_data.username,
        password=form_data.password)