from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(
        server_default="true",
        default=True,
    )
