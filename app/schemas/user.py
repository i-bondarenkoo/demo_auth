from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr


class CreateUserSchema(BaseModel):
    role_id: int
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    password_repeat: str


class ResponseUserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class LoginUserSchema(BaseModel):
    username: str
    password: str


class PatchUpdateUserSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
