from fastapi import APIRouter, Depends, HTTPException

from app.services.databases.repositories.category.category import CategoryCrud
from app.services.databases.schemas.category.category import CategoryModel
from app.services.security.permissions import get_current_active_superuser

router = APIRouter()


@router.post('/create', dependencies=[Depends(get_current_active_superuser)])
async def category_create(
        req: CategoryModel,
        crud: CategoryCrud = Depends()
):
    result = await crud.add_category(req)
    return result


@router.get('/list')
async def get_list(
        offset: int = 0,
        limit: int = 20,
        crud: CategoryCrud = Depends()
):
    result = await crud.get_list(
        limit=limit,
        offset=offset
    )
    return result


@router.delete('/delete/{cat_id}', dependencies=[Depends(get_current_active_superuser)])
async def delete_category(
        category_id: int,
        crud: CategoryCrud = Depends()
):
    result = await crud.delete_category(category_id=category_id)
    if result:
        return True
    return False


@router.get('/detail/{cat_id}')
async def get_category(
        category_id: int,
        crud: CategoryCrud = Depends()
):
    result = await crud.detail_category(category_id=category_id)
    if result:
        return result
    raise HTTPException(404, 'Category not found')


@router.patch('/update/{id}', dependencies=[Depends(get_current_active_superuser)])
async def update_category(
        cat_id: int, cat_model: CategoryModel,
        crud: CategoryCrud = Depends()
):
    result = await crud.update_category_by_id(cat_id, cat_model)
    if result:
        return result
    raise HTTPException(404, f'Category id {cat_id} does not found ')
