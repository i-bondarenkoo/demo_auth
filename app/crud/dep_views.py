from fastapi import Depends, HTTPException, status
from app.auth.dependencies import get_token_payload
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.database.db_constructor import db_constructor
from sqlalchemy import select
from app.models.role import Role


async def get_user_by_id_with_role_and_permission(
    token: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user_id: int = token["id"]
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(
            joinedload(User.role).options(
                selectinload(Role.access_role_rules),
            )
        )
    )
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user is None:
        return None
    return user


def validate_permission(element_id: int, action: str):
    async def check_permission_for_user(
        user: User = Depends(get_user_by_id_with_role_and_permission),
    ):
        for rule in user.role.access_role_rules:
            if rule.element_id == element_id and getattr(rule, action):
                return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для доступа к ресурсам",
        )

    return check_permission_for_user
