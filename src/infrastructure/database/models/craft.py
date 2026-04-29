from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric

from src.infrastructure.database.database_setup import BaseOrm


class CraftOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    raw_material_id: Mapped[int] = mapped_column(ForeignKey("raw_material.id"))
    amount_per_piece: Mapped[Decimal] = mapped_column(Numeric(10, 5))

    product: Mapped["ProductOrm"] = relationship()
    raw_material: Mapped["RawMaterialOrm"] = relationship()
