from fastapi import APIRouter, Depends, status, Path, HTTPException, Body
from app.crud.acess_rule import get_access_rule_by_id_crud, update_access_rule_crud
from app.database.db_constructor import db_constructor
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.access_rule import ResponseAccessRule, UpdateAccessRule
from typing import Annotated
from app.crud.dep_views import (
    validate_permission,
)
from app.utils.const import ACCESS_RULES, READ_ALL, UPDATE_ALL

router = APIRouter(
    prefix="/access_rules",
    tags=["AcessRules"],
)


@router.get("/{access_rule_id}", response_model=ResponseAccessRule)
async def get_access_rule_by_id(
    access_rule_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
    user: User = Depends(validate_permission(element_id=ACCESS_RULES, action=READ_ALL)),
):
    rules = await get_access_rule_by_id_crud(
        access_rule_id=access_rule_id,
        session=session,
    )
    if rules is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Набор правил не найден",
        )
    return rules


@router.patch("/{access_rule_id}", response_model=ResponseAccessRule)
async def update_acess_rule(
    access_rule_id: Annotated[int, Path(ge=1)],
    data_in: Annotated[UpdateAccessRule, Body()],
    session: AsyncSession = Depends(db_constructor.get_session),
    user: User = Depends(
        validate_permission(element_id=ACCESS_RULES, action=UPDATE_ALL)
    ),
):
    row_rule = await update_access_rule_crud(
        access_rule_id=access_rule_id,
        session=session,
        data_in=data_in,
    )
    if row_rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Набор правил не найден",
        )
    if row_rule == "no_data_to_update":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не переданы",
        )
    return row_rule
