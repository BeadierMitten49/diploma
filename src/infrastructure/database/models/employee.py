from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.infrastructure.database.database_setup import BaseOrm


class RoleOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    permissions: Mapped[list["RolePermissionOrm"]] = relationship(back_populates="role", cascade="all, delete-orphan")
    employees: Mapped[list["EmployeeOrm"]] = relationship(back_populates="role")


class RolePermissionOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    permission: Mapped[str]

    role: Mapped["RoleOrm"] = relationship(back_populates="permissions")


class EmployeeOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    role: Mapped["RoleOrm"] = relationship(back_populates="employees")
