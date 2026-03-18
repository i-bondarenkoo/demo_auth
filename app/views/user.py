from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Annotated
from app.schemas.user import CreateUserSchema, ResponseUserSchema, PatchUpdateUserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_constructor import db_constructor
from app.crud.user import create_user_crud, update_user_crud, deactivate_user_crud
from sqlalchemy.exc import IntegrityError
from app.auth.dependencies import get_current_user, get_current_active_user
from app.models.user import User
from app.crud.role import get_role_by_id_crud

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register", response_model=ResponseUserSchema)
async def create_user(
    user_in: Annotated[
        CreateUserSchema, Body(description="Данные пользователя для создания записи")
    ],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    check_role = await get_role_by_id_crud(role_id=user_in.role_id, session=session)
    if check_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Роль для пользователя не найдена",
        )
    if user_in.password != user_in.password_repeat:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароли не совпадают",
        )
    try:
        user = await create_user_crud(user_in=user_in, session=session)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такими данными уже существует",
        )
    return user


@router.patch("/me", response_model=ResponseUserSchema)
async def update_user(
    user_data: Annotated[
        PatchUpdateUserSchema, Body(description="Данные для обновления пользователя")
    ],
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    update_user = await update_user_crud(
        user_data=user_data,
        user=user,
        session=session,
    )
    if update_user == "not user_data":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не переданы",
        )
    return update_user


@router.delete("/me")
async def deactivate_user(
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    return await deactivate_user_crud(user=user, session=session)
