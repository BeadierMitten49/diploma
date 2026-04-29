from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal


@dataclass
class RawMaterial:
    """Справочник сырья."""
    id: int | None = field(default=None, kw_only=True)
    name: str
    critical_amount: Decimal  # кг
    shelf_life_days: int


@dataclass
class RawMaterialStock:
    """Складская запись сырья."""
    id: int | None = field(default=None, kw_only=True)
    raw_material: RawMaterial
    amount_kg: Decimal
    arrival_date: date
    comment: str = ""

    @property
    def expiry_date(self) -> date:
        return self.arrival_date + timedelta(days=self.raw_material.shelf_life_days)

    @property
    def is_critical(self) -> bool:
        return self.amount_kg <= self.raw_material.critical_amount

    @property
    def is_expired(self) -> bool:
        return date.today() >= self.expiry_date
