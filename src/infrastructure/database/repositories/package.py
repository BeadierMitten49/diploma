from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.domain.package import Package, PackageStock
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.package import PackageOrm, PackageStockOrm


def _to_package(orm: PackageOrm) -> Package:
    return Package(id=orm.id, name=orm.name, critical_amount=orm.critical_amount)


def _to_stock(orm: PackageStockOrm) -> PackageStock:
    return PackageStock(
        id=orm.id,
        package=_to_package(orm.package),
        amount=orm.amount,
        comment=orm.comment,
    )


class PackageRepository(Storage):
    async def get_all(self) -> list[Package]:
        async with self.session() as session:
            result = await session.execute(select(PackageOrm))
            return [_to_package(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Package | None:
        async with self.session() as session:
            orm = await session.get(PackageOrm, id)
            return _to_package(orm) if orm else None

    async def create(self, package: Package) -> Package:
        async with self.session() as session:
            orm = PackageOrm(name=package.name, critical_amount=package.critical_amount)
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return _to_package(orm)

    async def update(self, package: Package) -> Package:
        async with self.session() as session:
            orm = await session.get(PackageOrm, package.id)
            orm.name = package.name
            orm.critical_amount = package.critical_amount
            await session.commit()
            await session.refresh(orm)
            return _to_package(orm)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(PackageOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()


class PackageStockRepository(Storage):
    async def get_all(self) -> list[PackageStock]:
        async with self.session() as session:
            result = await session.execute(
                select(PackageStockOrm).options(selectinload(PackageStockOrm.package))
            )
            return [_to_stock(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> PackageStock | None:
        async with self.session() as session:
            result = await session.execute(
                select(PackageStockOrm)
                .options(selectinload(PackageStockOrm.package))
                .where(PackageStockOrm.id == id)
            )
            orm = result.scalar_one_or_none()
            return _to_stock(orm) if orm else None

    async def create(self, stock: PackageStock) -> PackageStock:
        async with self.session() as session:
            orm = PackageStockOrm(
                package_id=stock.package.id,
                amount=stock.amount,
                comment=stock.comment,
            )
            session.add(orm)
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update(self, stock: PackageStock) -> PackageStock:
        async with self.session() as session:
            orm = await session.get(PackageStockOrm, stock.id)
            orm.package_id = stock.package.id
            orm.amount = stock.amount
            orm.comment = stock.comment
            await session.commit()
            return await self.get_by_id(stock.id)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(PackageStockOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()
