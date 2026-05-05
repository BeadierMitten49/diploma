from src.domain.customer import Customer
from src.infrastructure.database.repositories.customer import CustomerRepository


class CustomerService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def get_customers(self) -> list[Customer]:
        return await self.customer_repo.get_all()

    async def get_customer(self, id: int) -> Customer | None:
        return await self.customer_repo.get_by_id(id)

    async def create_customer(self, customer: Customer) -> Customer:
        return await self.customer_repo.create(customer)

    async def update_customer(self, customer: Customer) -> Customer:
        return await self.customer_repo.update(customer)

    async def delete_customer(self, id: int) -> None:
        await self.customer_repo.delete(id)
