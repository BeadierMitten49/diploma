from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, Text

from src.infrastructure.database.database_setup import BaseOrm


class TaskOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    packaging_id: Mapped[int] = mapped_column(ForeignKey("packaging.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    planned_pieces: Mapped[int]
    planned_start_date: Mapped[date]
    deadline: Mapped[date]
    status: Mapped[str]
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    product: Mapped["ProductOrm"] = relationship()
    packaging: Mapped["PackagingOrm"] = relationship()
    employee: Mapped["EmployeeOrm"] = relationship()
    materials: Mapped[list["TaskMaterialOrm"]] = relationship(back_populates="task", cascade="all, delete-orphan")
    stops: Mapped[list["TaskStopOrm"]] = relationship(back_populates="task", cascade="all, delete-orphan")


class TaskMaterialOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    raw_material_id: Mapped[int] = mapped_column(ForeignKey("raw_material.id"))
    planned_amount: Mapped[Decimal] = mapped_column(Numeric(10, 3))

    task: Mapped["TaskOrm"] = relationship(back_populates="materials")
    raw_material: Mapped["RawMaterialOrm"] = relationship()


class TaskStopOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    reason: Mapped[str] = mapped_column(Text)
    stopped_at: Mapped[datetime]
    resumed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    task: Mapped["TaskOrm"] = relationship(back_populates="stops")
