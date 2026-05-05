from src.domain.raw_material import RawMaterial, RawMaterialStock
from src.infrastructure.database.repositories.raw_material import RawMaterialRepository, RawMaterialStockRepository


class RawMaterialService:
    def __init__(self, material_repo: RawMaterialRepository, stock_repo: RawMaterialStockRepository):
        self.material_repo = material_repo
        self.stock_repo = stock_repo

    async def get_materials(self) -> list[RawMaterial]:
        return await self.material_repo.get_all()

    async def get_material(self, id: int) -> RawMaterial | None:
        return await self.material_repo.get_by_id(id)

    async def create_material(self, material: RawMaterial) -> RawMaterial:
        return await self.material_repo.create(material)

    async def update_material(self, material: RawMaterial) -> RawMaterial:
        return await self.material_repo.update(material)

    async def delete_material(self, id: int) -> None:
        await self.material_repo.delete(id)

    async def get_stock(self) -> list[RawMaterialStock]:
        return await self.stock_repo.get_all()

    async def get_stock_item(self, id: int) -> RawMaterialStock | None:
        return await self.stock_repo.get_by_id(id)

    async def create_stock_item(self, stock: RawMaterialStock) -> RawMaterialStock:
        return await self.stock_repo.create(stock)

    async def update_stock_item(self, stock: RawMaterialStock) -> RawMaterialStock:
        return await self.stock_repo.update(stock)

    async def delete_stock_item(self, id: int) -> None:
        await self.stock_repo.delete(id)
