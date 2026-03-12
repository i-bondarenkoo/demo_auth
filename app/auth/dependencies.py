from fastapi import Form, Depends, HTTPException, status
from app.database.db_constructor import db_constructor
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_email_crud
from app.utils.helpers import verify_password


async def get_current_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ошибка авторизации",
    )
    user_db = await get_user_by_email_crud(email=username, session=session)
    if user_db is None:
        raise error
    if not verify_password(
        password=password,
        hashed_password=user_db.password_hash,
    ):
        raise error
    return user_db
