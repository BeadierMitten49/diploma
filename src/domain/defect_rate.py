from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class DefectRate:
    """Процент брака на всё производство."""
    id: int | None = field(default=None, kw_only=True)
    rate: Decimal  # например, Decimal("0.05") = 5%
