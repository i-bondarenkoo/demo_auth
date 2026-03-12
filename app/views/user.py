from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Annotated
from app.schemas.user import CreateUserSchema, ResponseUserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_constructor import db_constructor
from app.crud.user import create_user_crud
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=ResponseUserSchema)
async def create_user(
    user_in: Annotated[
        CreateUserSchema, Body(description="Данные пользователя для создания записи")
    ],
    session: AsyncSession = Depends(db_constructor.get_session),
):
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
