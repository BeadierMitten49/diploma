from enum import StrEnum
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from .employee import Employee
from .product import Product, Packaging
from .raw_material import RawMaterial


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    STOPPED = "stopped"
    COMPLETED = "completed"


@dataclass
class TaskMaterial:
    """Расчётное сырьё для задачи."""
    id: int | None = field(default=None, kw_only=True)
    raw_material: RawMaterial
    planned_amount: Decimal  # в кг


@dataclass
class TaskStop:
    """Остановка задачи."""
    id: int | None = field(default=None, kw_only=True)
    reason: str
    stopped_at: datetime
    resumed_at: datetime | None = None


@dataclass
class Task:
    """Задача производства."""
    id: int | None = field(default=None, kw_only=True)
    product: Product
    packaging: Packaging
    employee: Employee
    planned_pieces: int
    planned_start_date: date
    deadline: date
    status: TaskStatus
    materials: list[TaskMaterial]
    stops: list[TaskStop]
    comment: str | None = None

    @property
    def planned_boxes(self) -> int:
        return self.planned_pieces // self.packaging.pieces_per_box

    @property
    def planned_remainder_pieces(self) -> int:
        return self.planned_pieces % self.packaging.pieces_per_box
