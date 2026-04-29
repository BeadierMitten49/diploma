from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.infrastructure.database.database_setup import BaseOrm


class PackageOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    critical_amount: Mapped[int]

    stock: Mapped[list["PackageStockOrm"]] = relationship(back_populates="package")


class PackageStockOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("package.id"))
    amount: Mapped[int]
    comment: Mapped[str] = mapped_column(default="")

    package: Mapped["PackageOrm"] = relationship(back_populates="stock")
