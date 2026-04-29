from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.domain.raw_material import RawMaterial, RawMaterialStock
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.raw_material import RawMaterialOrm, RawMaterialStockOrm


def _to_material(orm: RawMaterialOrm) -> RawMaterial:
    return RawMaterial(
        id=orm.id,
        name=orm.name,
        critical_amount=orm.critical_amount,
        shelf_life_days=orm.shelf_life_days,
    )


def _to_stock(orm: RawMaterialStockOrm) -> RawMaterialStock:
    return RawMaterialStock(
        id=orm.id,
        raw_material=_to_material(orm.raw_material),
        amount_kg=orm.amount_kg,
        arrival_date=orm.arrival_date,
        comment=orm.comment,
    )


class RawMaterialRepository(Storage):
    async def get_all(self) -> list[RawMaterial]:
        async with self.session() as session:
            result = await session.execute(select(RawMaterialOrm))
            return [_to_material(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> RawMaterial | None:
        async with self.session() as session:
            orm = await session.get(RawMaterialOrm, id)
            return _to_material(orm) if orm else None

    async def create(self, material: RawMaterial) -> RawMaterial:
        async with self.session() as session:
            orm = RawMaterialOrm(
                name=material.name,
                critical_amount=material.critical_amount,
                shelf_life_days=material.shelf_life_days,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return _to_material(orm)

    async def update(self, material: RawMaterial) -> RawMaterial:
        async with self.session() as session:
            orm = await session.get(RawMaterialOrm, material.id)
            orm.name = material.name
            orm.critical_amount = material.critical_amount
            orm.shelf_life_days = material.shelf_life_days
            await session.commit()
            await session.refresh(orm)
            return _to_material(orm)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(RawMaterialOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()


class RawMaterialStockRepository(Storage):
    async def get_all(self) -> list[RawMaterialStock]:
        async with self.session() as session:
            result = await session.execute(
                select(RawMaterialStockOrm).options(selectinload(RawMaterialStockOrm.raw_material))
            )
            return [_to_stock(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> RawMaterialStock | None:
        async with self.session() as session:
            result = await session.execute(
                select(RawMaterialStockOrm)
                .options(selectinload(RawMaterialStockOrm.raw_material))
                .where(RawMaterialStockOrm.id == id)
            )
            orm = result.scalar_one_or_none()
            return _to_stock(orm) if orm else None

    async def create(self, stock: RawMaterialStock) -> RawMaterialStock:
        async with self.session() as session:
            orm = RawMaterialStockOrm(
                raw_material_id=stock.raw_material.id,
                amount_kg=stock.amount_kg,
                arrival_date=stock.arrival_date,
                comment=stock.comment,
            )
            session.add(orm)
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update(self, stock: RawMaterialStock) -> RawMaterialStock:
        async with self.session() as session:
            orm = await session.get(RawMaterialStockOrm, stock.id)
            orm.raw_material_id = stock.raw_material.id
            orm.amount_kg = stock.amount_kg
            orm.arrival_date = stock.arrival_date
            orm.comment = stock.comment
            await session.commit()
            return await self.get_by_id(stock.id)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(RawMaterialStockOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()
