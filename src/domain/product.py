from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Product:
    """Справочник продукции."""
    id: int | None = field(default=None, kw_only=True)
    name: str
    critical_amount: int  # штуки
    shelf_life_days: int


@dataclass
class Packaging:
    """Фасовка — количество штук продукта в коробке."""
    id: int | None = field(default=None, kw_only=True)
    product: Product
    pieces_per_box: int


@dataclass
class ProductStock:
    """Складская запись продукции."""
    id: int | None = field(default=None, kw_only=True)
    product: Product
    amount_pieces: int
    batch_number: str
    arrival_date: date
    packaging: Packaging
    comment: str = ""

    @property
    def expiry_date(self) -> date:
        return self.arrival_date + timedelta(days=self.product.shelf_life_days)

    @property
    def is_critical(self) -> bool:
        return self.amount_pieces <= self.product.critical_amount

    @property
    def is_expired(self) -> bool:
        return date.today() >= self.expiry_date

    @property
    def full_boxes(self) -> int:
        return self.amount_pieces // self.packaging.pieces_per_box

    @property
    def remaining_pieces(self) -> int:
        return self.amount_pieces % self.packaging.pieces_per_box
