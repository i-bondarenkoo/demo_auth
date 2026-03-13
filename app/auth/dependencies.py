from fastapi import Form, Depends, HTTPException, status
from app.database.db_constructor import db_constructor
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_email_crud, get_user_by_id_crud
from app.utils.helpers import verify_password
from app.models.user import User
from app.auth.jwt import decode_jwt
from jwt.exceptions import InvalidTokenError
from app.auth.security import oauth2_scheme


async def authenticate_user(
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
    if not user_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ошибка аутентификации, пользователь не активен",
        )
    if not verify_password(
        password=password,
        hashed_password=user_db.password_hash,
    ):
        raise error
    return user_db


async def get_token_payload(
    token=Depends(oauth2_scheme),
) -> dict:

    try:
        decode_token: dict = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
        )
    return decode_token


async def get_current_user(
    decode_token: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_constructor.get_session),
):

    user_id = decode_token["id"]
    user_db = await get_user_by_id_crud(user_id=user_id, session=session)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
        )
    return user_db


async def get_current_active_user(
    user: User = Depends(get_current_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Пользователь не активен",
    )
