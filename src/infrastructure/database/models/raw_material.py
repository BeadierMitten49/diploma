from decimal import Decimal
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric

from src.infrastructure.database.database_setup import BaseOrm


class RawMaterialOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    critical_amount: Mapped[Decimal] = mapped_column(Numeric(10, 3))
    shelf_life_days: Mapped[int]

    stock: Mapped[list["RawMaterialStockOrm"]] = relationship(back_populates="raw_material")


class RawMaterialStockOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    raw_material_id: Mapped[int] = mapped_column(ForeignKey("raw_material.id"))
    amount_kg: Mapped[Decimal] = mapped_column(Numeric(10, 3))
    arrival_date: Mapped[date]
    comment: Mapped[str] = mapped_column(default="")

    raw_material: Mapped["RawMaterialOrm"] = relationship(back_populates="stock")
