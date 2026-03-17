from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.access_role import AccessRole
from app.schemas.access_rule import UpdateAccessRule


async def get_access_rule_by_id_crud(access_rule_id: int, session: AsyncSession):
    # stmt = select(AccessRole).where(AccessRole.id == access_rule_id)
    # result = await session.execute(stmt)
    # rules = result.scalars().one_or_none()
    # return rules
    return await session.get(AccessRole, access_rule_id)


async def update_access_rule_crud(
    data_in: UpdateAccessRule,
    access_rule_id: int,
    session: AsyncSession,
):
    rule_row = await get_access_rule_by_id_crud(
        access_rule_id=access_rule_id,
        session=session,
    )
    if rule_row is None:
        return None
    data: dict = data_in.model_dump(exclude_unset=True)
    if len(data) == 0:
        return "no_data_to_update"
    for key, value in data.items():
        setattr(rule_row, key, value)

    await session.commit()
    await session.refresh(rule_row)
    return rule_row
