from pydantic import BaseModel
from pydantic import EmailStr


class CreateUserSchema(BaseModel):
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
