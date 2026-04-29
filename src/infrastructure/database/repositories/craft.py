from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.domain.craft import Craft
from src.domain.product import Product
from src.domain.raw_material import RawMaterial
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.craft import CraftOrm


def _to_craft(orm: CraftOrm) -> Craft:
    return Craft(
        id=orm.id,
        product=Product(
            id=orm.product.id,
            name=orm.product.name,
            critical_amount=orm.product.critical_amount,
            shelf_life_days=orm.product.shelf_life_days,
        ),
        raw_material=RawMaterial(
            id=orm.raw_material.id,
            name=orm.raw_material.name,
            critical_amount=orm.raw_material.critical_amount,
            shelf_life_days=orm.raw_material.shelf_life_days,
        ),
        amount_per_piece=orm.amount_per_piece,
    )


class CraftRepository(Storage):
    def _query(self):
        return select(CraftOrm).options(
            selectinload(CraftOrm.product),
            selectinload(CraftOrm.raw_material),
        )

    async def get_all(self) -> list[Craft]:
        async with self.session() as session:
            result = await session.execute(self._query())
            return [_to_craft(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Craft | None:
        async with self.session() as session:
            result = await session.execute(self._query().where(CraftOrm.id == id))
            orm = result.scalar_one_or_none()
            return _to_craft(orm) if orm else None

    async def get_by_product_id(self, product_id: int) -> list[Craft]:
        async with self.session() as session:
            result = await session.execute(
                self._query().where(CraftOrm.product_id == product_id)
            )
            return [_to_craft(row) for row in result.scalars().all()]

    async def create(self, craft: Craft) -> Craft:
        async with self.session() as session:
            orm = CraftOrm(
                product_id=craft.product.id,
                raw_material_id=craft.raw_material.id,
                amount_per_piece=craft.amount_per_piece,
            )
            session.add(orm)
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update(self, craft: Craft) -> Craft:
        async with self.session() as session:
            orm = await session.get(CraftOrm, craft.id)
            orm.product_id = craft.product.id
            orm.raw_material_id = craft.raw_material.id
            orm.amount_per_piece = craft.amount_per_piece
            await session.commit()
            return await self.get_by_id(craft.id)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(CraftOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()
