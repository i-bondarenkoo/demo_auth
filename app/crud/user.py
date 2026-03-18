from app.schemas.user import CreateUserSchema, PatchUpdateUserSchema
from app.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.helpers import hash_passwd

from sqlalchemy import select


async def create_user_crud(user_in: CreateUserSchema, session: AsyncSession):

    new_user = User(
        role_id=user_in.role_id,
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        password_hash=hash_passwd(user_in.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_id_crud(user_id: int, session: AsyncSession):
    return await session.get(User, user_id)


async def get_user_by_email_crud(email: str, session: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user is None:
        return None
    return user


async def update_user_crud(
    user_data: PatchUpdateUserSchema,
    session: AsyncSession,
    user: User,
):
    user_data: dict = user_data.model_dump(exclude_unset=True)
    if len(user_data) == 0:
        return "not user_data"
    if "password" in user_data:
        user.password_hash = hash_passwd(user_data["password"])
        user_data.pop("password")
    for key, value in user_data.items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user


async def deactivate_user_crud(user: User, session: AsyncSession):
    user.is_active = False
    await session.commit()
    await session.refresh(user)
    return {
        "message": "Аккаунт деактивирован",
    }
