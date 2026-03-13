import jwt
from app.core.config import settings
from datetime import datetime, timedelta
from app.models.user import User


def endode_jwt(
    payload: dict,
    key: str = settings.auth_jwt.key,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode: dict = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded_token = jwt.encode(
        payload=to_encode,
        key=key,
        algorithm=algorithm,
    )
    return encoded_token


def decode_jwt(
    token: str,
    key: str = settings.auth_jwt.key,
    algorithm: str = settings.auth_jwt.algorithm,
) -> str:
    decoded_token = jwt.decode(
        jwt=token,
        key=key,
        algorithms=[algorithm],
    )
    return decoded_token


def create_access_token(user: User) -> str:
    data: dict = {
        "id": user.id,
        # "first_name": user.first_name,
        # "last_name": user.last_name,
    }
    return endode_jwt(
        payload=data,
    )
