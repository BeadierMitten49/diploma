from dataclasses import dataclass, field
from decimal import Decimal

from .product import Product
from .raw_material import RawMaterial


@dataclass
class Craft:
    """Таблица расчёта затрат материалов (крафт)."""
    id: int | None = field(default=None, kw_only=True)
    product: Product
    raw_material: RawMaterial
    amount_per_piece: Decimal  # кг сырья на штуку продукта
