from typing import Optional, List, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.services.databases.schemas.product.product import (ProductCreateDTO,
                                                            ProductUpdateDTO,
                                                            ProductInDB)
from app.services.databases.repositories.product.product import ProductCrud
from app.services.security.permissions import get_current_active_superuser

router = APIRouter()


@router.post('/create', dependencies=[Depends(get_current_active_superuser)])
async def create_product(
        data: ProductCreateDTO,
        crud: ProductCrud = Depends()
) -> Optional[ProductInDB]:
    result = await crud.add_product(data=data)
    if result:
        return result
    raise HTTPException(404, 'Invalid data entered, category_id may be missing')


@router.get('/get_product/{product_id}')
async def get_product(
        product_id: int,
        crud: ProductCrud = Depends()
) -> ProductInDB:
    result = await crud.get_detail_product(product_id)
    if result:
        return result
    raise HTTPException(404, "Product does not exists")


@router.get('/list_product')
async def get_list(
        offset: int = 0,
        limit: int = 20,
        category_id: int = None,
        crud: ProductCrud = Depends()
) -> List[Optional[ProductInDB]]:
    result = await crud.get_list(
        offset=offset,
        limit=limit,
        category_id=category_id
    )
    return result


@router.delete('/delete/{product_id}', dependencies=[Depends(get_current_active_superuser)])
async def delete_product(
        product_id: int,
        crud: ProductCrud = Depends()
) -> Dict[str, str]:
    result = await crud.delete_product(product_id)
    if result:
        return {"message": "product successfully deleted"}
    raise HTTPException(404, "product does not exists")


@router.patch('/update/{product_id}', dependencies=[Depends(get_current_active_superuser)])
async def update_product(
        product_id: int,
        product_model: ProductUpdateDTO,
        crud: ProductCrud = Depends()
) -> ProductInDB:
    result = await crud.update_product(
        product_id=product_id,
        data=product_model)
    if result:
        return result
    raise HTTPException(404, f'Category id {product_id} does not found ')
