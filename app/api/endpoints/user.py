from fastapi import APIRouter, Depends
from app.databases.schemas.user.user import UserCreate
from app.databases.repositories.user.user import UserCrud


router = APIRouter()


@router.post('/create')
async def user_create(req: UserCreate,
                          crud: UserCrud = Depends()):
    result = await crud.create_user(req)
    return result
