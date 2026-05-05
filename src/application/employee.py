from src.domain.employee import Role, Employee
from src.infrastructure.database.repositories.employee import RoleRepository, EmployeeRepository


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    async def get_roles(self) -> list[Role]:
        return await self.role_repo.get_all()

    async def get_role(self, id: int) -> Role | None:
        return await self.role_repo.get_by_id(id)

    async def create_role(self, role: Role) -> Role:
        return await self.role_repo.create(role)

    async def update_role(self, role: Role) -> Role:
        return await self.role_repo.update(role)

    async def delete_role(self, id: int) -> None:
        await self.role_repo.delete(id)


class EmployeeService:
    def __init__(self, employee_repo: EmployeeRepository):
        self.employee_repo = employee_repo

    async def get_employees(self) -> list[Employee]:
        return await self.employee_repo.get_all()

    async def get_employee(self, id: int) -> Employee | None:
        return await self.employee_repo.get_by_id(id)

    async def create_employee(self, employee: Employee) -> Employee:
        return await self.employee_repo.create(employee)

    async def update_employee(self, employee: Employee) -> Employee:
        return await self.employee_repo.update(employee)

    async def delete_employee(self, id: int) -> None:
        await self.employee_repo.delete(id)
