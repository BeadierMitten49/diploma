from sqlalchemy import select

from src.domain.defect_rate import DefectRate
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.defect_rate import DefectRateOrm


def _to_defect_rate(orm: DefectRateOrm) -> DefectRate:
    return DefectRate(id=orm.id, rate=orm.rate)


class DefectRateRepository(Storage):
    async def get(self) -> DefectRate | None:
        async with self.session() as session:
            result = await session.execute(select(DefectRateOrm).limit(1))
            orm = result.scalar_one_or_none()
            return _to_defect_rate(orm) if orm else None

    async def update(self, defect_rate: DefectRate) -> DefectRate:
        async with self.session() as session:
            orm = await session.get(DefectRateOrm, defect_rate.id)
            orm.rate = defect_rate.rate
            await session.commit()
            await session.refresh(orm)
            return _to_defect_rate(orm)
