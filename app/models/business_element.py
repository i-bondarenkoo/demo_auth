from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.access_role import AccessRole


class BusinessElement(Base):
    __tablename__ = "business_elements"
    name: Mapped[str] = mapped_column(String(35), unique=True)

    access_role_rules: Mapped[list["AccessRole"]] = relationship(
        "AccessRole",
        back_populates="business_element",
        cascade="all, delete-orphan",
    )
