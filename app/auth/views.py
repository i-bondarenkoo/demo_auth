from fastapi import APIRouter, Depends
from app.schemas.token import ResponseTokenSchema
from app.schemas.user import LoginUserSchema
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=ResponseTokenSchema)
async def login(user: User = Depends(get_current_user)):
    access_token: str = create_access_token(user)
    return ResponseTokenSchema(
        access_token=access_token,
    )
