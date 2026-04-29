from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric

from src.infrastructure.database.database_setup import BaseOrm


class DefectRateOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    rate: Mapped[Decimal] = mapped_column(Numeric(5, 4))
