from app.schemas.user import CreateUserSchema
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.helpers import hash_passwd


async def create_user_crud(user_in: CreateUserSchema, session: AsyncSession):

    new_user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        password_hash=hash_passwd(user_in.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email_crud(email: str, session: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user is None:
        return None
    return user
