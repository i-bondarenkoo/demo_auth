from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from app.models.user import User
from typing import Annotated
from app.schemas.product import ResponseProduct, PatchProductUpdate
from app.crud.dep_views import validate_permission
from app.utils.const import READ, READ_ALL, UPDATE, PRODUCT

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(
    user: User = Depends(validate_permission(element_id=PRODUCT, action=READ_ALL)),
):
    product1 = ResponseProduct(
        id=2,
        name="Молоко",
        price=123,
    )
    product2 = ResponseProduct(
        id=5,
        name="Хлеб",
        price=45,
    )
    return [product1, product2]


@router.patch("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: Annotated[
        int, Path(ge=1, description="ID продукта для обновления информации")
    ],
    product_in: Annotated[PatchProductUpdate, Body()],
    user: User = Depends(validate_permission(element_id=PRODUCT, action=UPDATE)),
):
    data: dict = product_in.model_dump(exclude_unset=True)
    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновление не переданы",
        )
    name = data.get("name", "Хлеб")
    price = data.get("price", 45)
    if price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Цена должна быть больше 0",
        )
    return ResponseProduct(
        id=product_id,
        name=name,
        price=price,
    )


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: Annotated[
        int, Path(ge=1, description="ID продукта для получения информации")
    ],
    user: User = Depends(validate_permission(element_id=PRODUCT, action=READ)),
):
    return ResponseProduct(
        id=product_id,
        name="Молоко",
        price=123,
    )
