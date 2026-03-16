from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.business_element import BusinessElement


class AccessRole(Base):
    __tablename__ = "access_role_rules"
    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "element_id",
            name="uq_role_element",
        ),
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    element_id: Mapped[int] = mapped_column(
        ForeignKey("business_elements.id", ondelete="CASCADE")
    )
    read_permission: Mapped[bool] = mapped_column(default=False, server_default="false")
    read_all_permission: Mapped[bool] = mapped_column(
        default=False, server_default="false"
    )
    create_permission: Mapped[bool] = mapped_column(
        default=False, server_default="false"
    )
    update_permission: Mapped[bool] = mapped_column(
        default=False, server_default="false"
    )
    update_all_permission: Mapped[bool] = mapped_column(
        default=False, server_default="false"
    )
    delete_permission: Mapped[bool] = mapped_column(
        default=False, server_default="false"
    )
    delete_all_permission: Mapped[bool] = mapped_column(
        default=False, server_default="false"
    )

    role: Mapped["Role"] = relationship("Role", back_populates="access_role_rules")
    business_element: Mapped["BusinessElement"] = relationship(
        "BusinessElement", back_populates="access_role_rules"
    )
