from app.models.business_element import BusinessElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_business_element_by_id_crud(elemnt_id: int, session: AsyncSession):
    return await session.get(BusinessElement, elemnt_id)
