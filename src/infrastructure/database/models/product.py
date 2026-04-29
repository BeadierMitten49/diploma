from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.infrastructure.database.database_setup import BaseOrm


class ProductOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    critical_amount: Mapped[int]
    shelf_life_days: Mapped[int]

    packaging: Mapped["PackagingOrm"] = relationship(back_populates="product", uselist=False)
    stock: Mapped[list["ProductStockOrm"]] = relationship(back_populates="product")


class PackagingOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    pieces_per_box: Mapped[int]

    product: Mapped["ProductOrm"] = relationship(back_populates="packaging")


class ProductStockOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    amount_pieces: Mapped[int]
    batch_number: Mapped[str]
    arrival_date: Mapped[date]
    comment: Mapped[str] = mapped_column(default="")

    product: Mapped["ProductOrm"] = relationship(back_populates="stock")
