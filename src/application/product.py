from src.domain.product import Product, Packaging, ProductStock
from src.infrastructure.database.repositories.product import (
    ProductRepository,
    PackagingRepository,
    ProductStockRepository,
)


class ProductService:
    def __init__(
        self,
        product_repo: ProductRepository,
        packaging_repo: PackagingRepository,
        stock_repo: ProductStockRepository,
    ):
        self.product_repo = product_repo
        self.packaging_repo = packaging_repo
        self.stock_repo = stock_repo

    async def get_products(self) -> list[Product]:
        return await self.product_repo.get_all()

    async def get_product(self, id: int) -> Product | None:
        return await self.product_repo.get_by_id(id)

    async def create_product(self, product: Product) -> Product:
        return await self.product_repo.create(product)

    async def update_product(self, product: Product) -> Product:
        return await self.product_repo.update(product)

    async def delete_product(self, id: int) -> None:
        await self.product_repo.delete(id)

    async def get_packagings(self) -> list[Packaging]:
        return await self.packaging_repo.get_all()

    async def get_packaging(self, id: int) -> Packaging | None:
        return await self.packaging_repo.get_by_id(id)

    async def get_packaging_by_product(self, product_id: int) -> Packaging | None:
        return await self.packaging_repo.get_by_product_id(product_id)

    async def create_packaging(self, packaging: Packaging) -> Packaging:
        return await self.packaging_repo.create(packaging)

    async def update_packaging(self, packaging: Packaging) -> Packaging:
        return await self.packaging_repo.update(packaging)

    async def delete_packaging(self, id: int) -> None:
        await self.packaging_repo.delete(id)

    async def get_stock(self) -> list[ProductStock]:
        return await self.stock_repo.get_all()

    async def get_stock_item(self, id: int) -> ProductStock | None:
        return await self.stock_repo.get_by_id(id)

    async def create_stock_item(self, stock: ProductStock) -> ProductStock:
        return await self.stock_repo.create(stock)

    async def update_stock_item(self, stock: ProductStock) -> ProductStock:
        return await self.stock_repo.update(stock)

    async def delete_stock_item(self, id: int) -> None:
        await self.stock_repo.delete(id)
