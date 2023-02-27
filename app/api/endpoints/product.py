from fastapi import APIRouter, Depends, HTTPException
from app.databases.schemas.product.product import ProductModel
from app.databases.repositories.product.productcrud import ProductCrud


router = APIRouter()


@router.post('/create')
async def product_create(req: ProductModel,
                          crud: ProductCrud = Depends()):
    result = await crud.add_product(req)
    return result


@router.get('/get_product/{product_id}')
async def get_product(product_id: int,
                      crud: ProductCrud = Depends()):
    result = await crud.get_product(product_id)
    return result


@router.get('/all_product')
async def get_all_product(offset: int = 0,
                          limit: int = 20,
                          crud: ProductCrud = Depends()):
    result = await crud.get_all_product(offset, limit)
    return result


@router.get('/all_product_by_category/{category_id}')
async def get_all_product_by_category(category_id: int,
                          offset: int = 0,
                          limit: int = 20,
                          crud: ProductCrud = Depends()):
    result = await crud.get_all_product_by_category(category_id,
                                                    offset,
                                                    limit)
    if result:
        return result
    return 'Product does not exist'


@router.delete('/delete/{product_id}')
async def delete_product(product_id: int,
                         crud: ProductCrud = Depends()):
    result = await crud.delete_product(product_id)
    if result:
        return True
    return False


@router.patch('/update/{product_id}')
async def update_product(product_id: int,
                         product_model: ProductModel,
                         crud: ProductCrud = Depends()):
    result = await crud.update_product(product_id, product_model)
    if result:
        return result
    raise HTTPException(404, f'Category id {product_id} does not found ')