import jwt
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from app.databases.repositories.user.user import UserCrud
from app.core.jwt import ALGORITHM
from app.core.settings import SECRET_KEY
from app.databases.schemas.tokens.tokens import TokenPayload
from app.databases.schemas.user.user import UserInDB

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


async def get_current_user(crud: UserCrud = Depends(UserCrud),
                          token: str = Security(reusable_oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await crud.get(user_id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(current_user: UserInDB = Security(get_current_user),
                            crud: UserCrud = Depends(UserCrud)):
    if not await crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: UserInDB = Security(get_current_user),
                                 crud: UserCrud = Depends(UserCrud)):
    if not await crud.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user