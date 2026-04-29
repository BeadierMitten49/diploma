from sqlalchemy import select

from src.domain.customer import Customer
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.customer import CustomerOrm


def _to_customer(orm: CustomerOrm) -> Customer:
    return Customer(id=orm.id, name=orm.name, address=orm.address, comment=orm.comment)


class CustomerRepository(Storage):
    async def get_all(self) -> list[Customer]:
        async with self.session() as session:
            result = await session.execute(select(CustomerOrm))
            return [_to_customer(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Customer | None:
        async with self.session() as session:
            orm = await session.get(CustomerOrm, id)
            return _to_customer(orm) if orm else None

    async def create(self, customer: Customer) -> Customer:
        async with self.session() as session:
            orm = CustomerOrm(
                name=customer.name,
                address=customer.address,
                comment=customer.comment,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return _to_customer(orm)

    async def update(self, customer: Customer) -> Customer:
        async with self.session() as session:
            orm = await session.get(CustomerOrm, customer.id)
            orm.name = customer.name
            orm.address = customer.address
            orm.comment = customer.comment
            await session.commit()
            await session.refresh(orm)
            return _to_customer(orm)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(CustomerOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()
