from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.access_rule import AccessRule


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(35), unique=True)

    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
    )

    access_role_rules: Mapped[list["AccessRule"]] = relationship(
        "AccessRule",
        back_populates="role",
        cascade="all, delete-orphan",
    )
