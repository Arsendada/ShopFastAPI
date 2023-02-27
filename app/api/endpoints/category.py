from fastapi import APIRouter, Depends, HTTPException
from app.databases.repositories.product.categorycrud import CategoryCrud
from app.databases.schemas.product.category import CategoryModel

router = APIRouter()


@router.post('/create')
async def category_create(req: CategoryModel,
                          crud: CategoryCrud = Depends(CategoryCrud)):
    result = await crud.add_category(req)
    return result


@router.get('/all')
async def get_category_list(crud: CategoryCrud = Depends(CategoryCrud)):
    result = await crud.get_all_category()
    return result


@router.delete('/delete/{cat_id}')
async def delete_category(cat_id: int,
                          crud: CategoryCrud = Depends(CategoryCrud)):
    result = await crud.delete_category(cat_id)
    if result:
        return True
    return False


@router.get('/get_category/{cat_id}')
async def get_category(cat_id: int,
                       crud: CategoryCrud = Depends(CategoryCrud)):
    result = await crud.get_category_by_id(cat_id)
    if result:
        return result
    raise HTTPException(404, 'Category not found')


@router.patch('/update/{id}')
async def update_category(cat_id: int, cat_model: CategoryModel,
                             crud: CategoryCrud = Depends(CategoryCrud)):
    result = await crud.update_category_by_id(cat_id, cat_model)
    if result:
        return result
    raise HTTPException(404, f'Category id {cat_id} does not found ')