from fastapi import APIRouter, Depends, status, Path, HTTPException, Body
from app.crud.acess_rule import (
    get_access_rule_by_id_crud,
    update_access_rule_crud,
    create_access_rule_crud,
    delete_access_rule_crud,
)
from sqlalchemy.exc import IntegrityError
from app.database.db_constructor import db_constructor
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.access_rule import (
    ResponseAccessRule,
    UpdateAccessRule,
    CreateAccessRule,
)
from typing import Annotated
from app.crud.dep_views import (
    validate_permission,
)
from app.crud.role import get_role_by_id_crud
from app.crud.business_element import get_business_element_by_id_crud
from app.utils.const import ACCESS_RULES, READ_ALL, UPDATE_ALL, CREATE, DELETE_ALL

router = APIRouter(
    prefix="/access_rules",
    tags=["AcessRules"],
)


@router.post("/", response_model=ResponseAccessRule)
async def create_access_rule(
    data_in: Annotated[CreateAccessRule, Body()],
    session: AsyncSession = Depends(db_constructor.get_session),
    user: User = Depends(validate_permission(element_id=ACCESS_RULES, action=CREATE)),
):
    check_element = await get_business_element_by_id_crud(
        elemnt_id=data_in.element_id, session=session
    )
    if check_element is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект не найден",
        )
    check_role = await get_role_by_id_crud(role_id=data_in.role_id, session=session)
    if check_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект  не найден",
        )
    try:
        new_row = await create_access_rule_crud(data_in=data_in, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Правило уже существует в таблице",
        )
    return new_row


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


@router.delete("/{access_rule_id}")
async def delete_access_rule(
    access_rule_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
    user: User = Depends(
        validate_permission(element_id=ACCESS_RULES, action=DELETE_ALL)
    ),
):
    access_rule = await delete_access_rule_crud(
        access_rule_id=access_rule_id, session=session
    )
    if access_rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Набор правил не найден",
        )
    return access_rule
