from fastapi import APIRouter, Depends, status
from app.models.user import User
from app.schemas.category import ResponseCategory
from app.crud.dep_views import all_read_permission_checker

router = APIRouter(
    prefix="/categories",
    tags=["Category"],
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_category(
    user: User = Depends(all_read_permission_checker(element_idx=3)),
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
