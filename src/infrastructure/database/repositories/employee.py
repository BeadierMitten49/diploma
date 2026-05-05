from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.domain.employee import Permission, Role, Employee
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.employee import RoleOrm, RolePermissionOrm, EmployeeOrm


def _to_role(orm: RoleOrm) -> Role:
    return Role(
        id=orm.id,
        name=orm.name,
        permissions=[Permission(p.permission) for p in orm.permissions],
    )


def _to_employee(orm: EmployeeOrm) -> Employee:
    return Employee(
        id=orm.id,
        name=orm.name,
        role=_to_role(orm.role),
    )


class RoleRepository(Storage):
    def _query(self):
        return select(RoleOrm).options(selectinload(RoleOrm.permissions))

    async def get_all(self) -> list[Role]:
        async with self.session() as session:
            result = await session.execute(self._query())
            return [_to_role(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Role | None:
        async with self.session() as session:
            result = await session.execute(self._query().where(RoleOrm.id == id))
            orm = result.scalar_one_or_none()
            return _to_role(orm) if orm else None

    async def create(self, role: Role) -> Role:
        async with self.session() as session:
            orm = RoleOrm(name=role.name)
            session.add(orm)
            await session.flush()
            for p in role.permissions:
                session.add(RolePermissionOrm(role_id=orm.id, permission=str(p)))
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update(self, role: Role) -> Role:
        async with self.session() as session:
            orm = await session.get(RoleOrm, role.id)
            orm.name = role.name
            await session.execute(
                delete(RolePermissionOrm).where(RolePermissionOrm.role_id == role.id)
            )
            for p in role.permissions:
                session.add(RolePermissionOrm(role_id=role.id, permission=str(p)))
            await session.commit()
            return await self.get_by_id(role.id)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(RoleOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()


class EmployeeRepository(Storage):
    def _query(self):
        return select(EmployeeOrm).options(
            selectinload(EmployeeOrm.role).selectinload(RoleOrm.permissions)
        )

    async def get_all(self) -> list[Employee]:
        async with self.session() as session:
            result = await session.execute(self._query())
            return [_to_employee(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Employee | None:
        async with self.session() as session:
            result = await session.execute(self._query().where(EmployeeOrm.id == id))
            orm = result.scalar_one_or_none()
            return _to_employee(orm) if orm else None

    async def create(self, employee: Employee) -> Employee:
        async with self.session() as session:
            orm = EmployeeOrm(name=employee.name, role_id=employee.role.id)
            session.add(orm)
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update(self, employee: Employee) -> Employee:
        async with self.session() as session:
            orm = await session.get(EmployeeOrm, employee.id)
            orm.name = employee.name
            orm.role_id = employee.role.id
            await session.commit()
            return await self.get_by_id(employee.id)

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(EmployeeOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()
