from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.domain.product import Product, Packaging, ProductStock
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.product import ProductOrm, PackagingOrm, ProductStockOrm


def _to_product(orm: ProductOrm) -> Product:
    return Product(
        id=orm.id,
        name=orm.name,
        critical_amount=orm.critical_amount,
        shelf_life_days=orm.shelf_life_days,
    )


def _to_packaging(orm: PackagingOrm) -> Packaging:
    return Packaging(
        id=orm.id,
        product=_to_product(orm.product),
        pieces_per_box=orm.pieces_per_box,
    )


def _to_stock(orm: ProductStockOrm) -> ProductStock:
    return ProductStock(
        id=orm.id,
        product=_to_product(orm.product),
        amount_pieces=orm.amount_pieces,
        batch_number=orm.batch_number,
        arrival_date=orm.arrival_date,
        packaging=_to_packaging(orm.product.packaging),
        comment=orm.comment,
    )


class ProductRepository(Storage):
    async def get_all(self) -> list[Product]:
        async with self.session() as session:
            result = await session.execute(select(ProductOrm))
            return [_to_product(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Product | None:
        async with self.session() as session:
            orm = await session.get(ProductOrm, id)
            return _to_product(orm) if orm else None

    async def create(self, product: Product) -> Product:
        async with self.session() as session:
            orm = ProductOrm(
                name=product.name,
                critical_amount=product.critical_amount,
                shelf_life_days=product.shelf_life_days,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return _to_product(orm)

    async def update(self, product: Product) -> Product:
        async with self.session() as session:
            orm = await session.get(ProductOrm, product.id)
            orm.name = product.name
            orm.critical_amount = product.critical_amount
            orm.shelf_life_days = product.shelf_life_days
            await session.commit()
            await session.refresh(orm)
            return _to_product(orm)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(ProductOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()


class PackagingRepository(Storage):
    async def get_all(self) -> list[Packaging]:
        async with self.session() as session:
            result = await session.execute(
                select(PackagingOrm).options(selectinload(PackagingOrm.product))
            )
            return [_to_packaging(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Packaging | None:
        async with self.session() as session:
            result = await session.execute(
                select(PackagingOrm)
                .options(selectinload(PackagingOrm.product))
                .where(PackagingOrm.id == id)
            )
            orm = result.scalar_one_or_none()
            return _to_packaging(orm) if orm else None

    async def get_by_product_id(self, product_id: int) -> Packaging | None:
        async with self.session() as session:
            result = await session.execute(
                select(PackagingOrm)
                .options(selectinload(PackagingOrm.product))
                .where(PackagingOrm.product_id == product_id)
            )
            orm = result.scalar_one_or_none()
            return _to_packaging(orm) if orm else None

    async def create(self, packaging: Packaging) -> Packaging:
        async with self.session() as session:
            orm = PackagingOrm(
                product_id=packaging.product.id,
                pieces_per_box=packaging.pieces_per_box,
            )
            session.add(orm)
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update(self, packaging: Packaging) -> Packaging:
        async with self.session() as session:
            orm = await session.get(PackagingOrm, packaging.id)
            orm.product_id = packaging.product.id
            orm.pieces_per_box = packaging.pieces_per_box
            await session.commit()
            return await self.get_by_id(packaging.id)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(PackagingOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()


class ProductStockRepository(Storage):
    def _query(self):
        return select(ProductStockOrm).options(
            selectinload(ProductStockOrm.product).selectinload(ProductOrm.packaging)
        )

    async def get_all(self) -> list[ProductStock]:
        async with self.session() as session:
            result = await session.execute(self._query())
            return [_to_stock(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> ProductStock | None:
        async with self.session() as session:
            result = await session.execute(self._query().where(ProductStockOrm.id == id))
            orm = result.scalar_one_or_none()
            return _to_stock(orm) if orm else None

    async def create(self, stock: ProductStock) -> ProductStock:
        async with self.session() as session:
            orm = ProductStockOrm(
                product_id=stock.product.id,
                amount_pieces=stock.amount_pieces,
                batch_number=stock.batch_number,
                arrival_date=stock.arrival_date,
                comment=stock.comment,
            )
            session.add(orm)
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update(self, stock: ProductStock) -> ProductStock:
        async with self.session() as session:
            orm = await session.get(ProductStockOrm, stock.id)
            orm.product_id = stock.product.id
            orm.amount_pieces = stock.amount_pieces
            orm.batch_number = stock.batch_number
            orm.arrival_date = stock.arrival_date
            orm.comment = stock.comment
            await session.commit()
            return await self.get_by_id(stock.id)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(ProductStockOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()
