from src.domain.craft import Craft
from src.infrastructure.database.repositories.craft import CraftRepository


class CraftService:
    def __init__(self, craft_repo: CraftRepository):
        self.craft_repo = craft_repo

    async def get_crafts(self) -> list[Craft]:
        return await self.craft_repo.get_all()

    async def get_craft(self, id: int) -> Craft | None:
        return await self.craft_repo.get_by_id(id)

    async def get_crafts_by_product(self, product_id: int) -> list[Craft]:
        return await self.craft_repo.get_by_product_id(product_id)

    async def create_craft(self, craft: Craft) -> Craft:
        return await self.craft_repo.create(craft)

    async def update_craft(self, craft: Craft) -> Craft:
        return await self.craft_repo.update(craft)

    async def delete_craft(self, id: int) -> None:
        await self.craft_repo.delete(id)
