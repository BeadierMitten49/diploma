from dataclasses import dataclass, field


@dataclass
class Customer:
    """Заказчики."""
    id: int | None = field(default=None, kw_only=True)
    name: str
    address: str
    comment: str = ""
