from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.access_rule import AccessRule


class BusinessElement(Base):
    __tablename__ = "business_elements"
    name: Mapped[str] = mapped_column(String(35), unique=True)

    access_role_rules: Mapped[list["AccessRule"]] = relationship(
        "AccessRule",
        back_populates="business_element",
        cascade="all, delete-orphan",
    )
