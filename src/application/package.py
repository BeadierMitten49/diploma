from src.domain.package import Package, PackageStock
from src.infrastructure.database.repositories.package import PackageRepository, PackageStockRepository


class PackageService:
    def __init__(self, package_repo: PackageRepository, stock_repo: PackageStockRepository):
        self.package_repo = package_repo
        self.stock_repo = stock_repo

    async def get_packages(self) -> list[Package]:
        return await self.package_repo.get_all()

    async def get_package(self, id: int) -> Package | None:
        return await self.package_repo.get_by_id(id)

    async def create_package(self, package: Package) -> Package:
        return await self.package_repo.create(package)

    async def update_package(self, package: Package) -> Package:
        return await self.package_repo.update(package)

    async def delete_package(self, id: int) -> None:
        await self.package_repo.delete(id)

    async def get_stock(self) -> list[PackageStock]:
        return await self.stock_repo.get_all()

    async def get_stock_item(self, id: int) -> PackageStock | None:
        return await self.stock_repo.get_by_id(id)

    async def create_stock_item(self, stock: PackageStock) -> PackageStock:
        return await self.stock_repo.create(stock)

    async def update_stock_item(self, stock: PackageStock) -> PackageStock:
        return await self.stock_repo.update(stock)

    async def delete_stock_item(self, id: int) -> None:
        await self.stock_repo.delete(id)
