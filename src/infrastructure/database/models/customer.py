from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.database_setup import BaseOrm


class CustomerOrm(BaseOrm):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str]
    comment: Mapped[str] = mapped_column(default="")
