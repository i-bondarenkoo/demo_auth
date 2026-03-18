from app.models.role import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_role_by_id_crud(role_id: int, session: AsyncSession):
    return await session.get(Role, role_id)
