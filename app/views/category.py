from fastapi import APIRouter, Depends, status, Body, Path
from app.models.user import User
from typing import Annotated
from app.schemas.category import ResponseCategory, CreateCategory
from app.crud.dep_views import validate_permission
from app.utils.const import READ_ALL, CATEGORY, DELETE_ALL, CREATE

router = APIRouter(
    prefix="/categories",
    tags=["Category"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    data_in: Annotated[CreateCategory, Body()],
    user: User = Depends(validate_permission(element_id=CATEGORY, action=CREATE)),
):
    new_category = ResponseCategory(
        id=4,
        category_type=data_in.category_type,
        count_instance=data_in.count_instance,
    )
    return new_category


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_category(
    user: User = Depends(validate_permission(element_id=CATEGORY, action=READ_ALL)),
):
    category1 = ResponseCategory(
        id=2,
        category_type="Товары для дома",
        count_instance=25,
    )
    category2 = ResponseCategory(
        id=5,
        category_type="Бижутерия",
        count_instance=35,
    )
    return [category1, category2]


@router.delete("/{category_id}")
async def delete_category_by_id(
    category_id: Annotated[int, Path(ge=1)],
    user: User = Depends(validate_permission(element_id=CATEGORY, action=DELETE_ALL)),
):
    return {
        "message": "категория удалена",
    }
