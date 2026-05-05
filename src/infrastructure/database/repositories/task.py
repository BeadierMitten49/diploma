from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.domain.employee import Permission, Role, Employee
from src.domain.product import Product, Packaging
from src.domain.raw_material import RawMaterial
from src.domain.task import Task, TaskMaterial, TaskStatus, TaskStop
from src.infrastructure.database.database_setup import Storage
from src.infrastructure.database.models.employee import RoleOrm, EmployeeOrm
from src.infrastructure.database.models.product import PackagingOrm
from src.infrastructure.database.models.task import TaskOrm, TaskMaterialOrm, TaskStopOrm


def _to_task_material(orm: TaskMaterialOrm) -> TaskMaterial:
    return TaskMaterial(
        id=orm.id,
        raw_material=RawMaterial(
            id=orm.raw_material.id,
            name=orm.raw_material.name,
            critical_amount=orm.raw_material.critical_amount,
            shelf_life_days=orm.raw_material.shelf_life_days,
        ),
        planned_amount=orm.planned_amount,
    )


def _to_task_stop(orm: TaskStopOrm) -> TaskStop:
    return TaskStop(
        id=orm.id,
        reason=orm.reason,
        stopped_at=orm.stopped_at,
        resumed_at=orm.resumed_at,
    )


def _to_task(orm: TaskOrm) -> Task:
    return Task(
        id=orm.id,
        product=Product(
            id=orm.product.id,
            name=orm.product.name,
            critical_amount=orm.product.critical_amount,
            shelf_life_days=orm.product.shelf_life_days,
        ),
        packaging=Packaging(
            id=orm.packaging.id,
            product=Product(
                id=orm.packaging.product.id,
                name=orm.packaging.product.name,
                critical_amount=orm.packaging.product.critical_amount,
                shelf_life_days=orm.packaging.product.shelf_life_days,
            ),
            pieces_per_box=orm.packaging.pieces_per_box,
        ),
        employee=Employee(
            id=orm.employee.id,
            name=orm.employee.name,
            role=Role(
                id=orm.employee.role.id,
                name=orm.employee.role.name,
                permissions=[Permission(p.permission) for p in orm.employee.role.permissions],
            ),
        ),
        planned_pieces=orm.planned_pieces,
        planned_start_date=orm.planned_start_date,
        deadline=orm.deadline,
        status=TaskStatus(orm.status),
        materials=[_to_task_material(m) for m in orm.materials],
        stops=[_to_task_stop(s) for s in orm.stops],
        comment=orm.comment,
    )


class TaskRepository(Storage):
    def _query(self):
        return select(TaskOrm).options(
            selectinload(TaskOrm.product),
            selectinload(TaskOrm.packaging).selectinload(PackagingOrm.product),
            selectinload(TaskOrm.employee).selectinload(EmployeeOrm.role).selectinload(RoleOrm.permissions),
            selectinload(TaskOrm.materials).selectinload(TaskMaterialOrm.raw_material),
            selectinload(TaskOrm.stops),
        )

    async def get_all(self) -> list[Task]:
        async with self.session() as session:
            result = await session.execute(self._query())
            return [_to_task(row) for row in result.scalars().all()]

    async def get_by_id(self, id: int) -> Task | None:
        async with self.session() as session:
            result = await session.execute(self._query().where(TaskOrm.id == id))
            orm = result.scalar_one_or_none()
            return _to_task(orm) if orm else None

    async def get_by_status(self, status: TaskStatus) -> list[Task]:
        async with self.session() as session:
            result = await session.execute(
                self._query().where(TaskOrm.status == str(status))
            )
            return [_to_task(row) for row in result.scalars().all()]

    async def create(self, task: Task) -> Task:
        async with self.session() as session:
            orm = TaskOrm(
                product_id=task.product.id,
                packaging_id=task.packaging.id,
                employee_id=task.employee.id,
                planned_pieces=task.planned_pieces,
                planned_start_date=task.planned_start_date,
                deadline=task.deadline,
                status=str(task.status),
                comment=task.comment,
            )
            session.add(orm)
            await session.flush()
            for m in task.materials:
                session.add(TaskMaterialOrm(
                    task_id=orm.id,
                    raw_material_id=m.raw_material.id,
                    planned_amount=m.planned_amount,
                ))
            await session.commit()
            return await self.get_by_id(orm.id)

    async def update_status(self, task_id: int, status: TaskStatus) -> Task:
        async with self.session() as session:
            orm = await session.get(TaskOrm, task_id)
            orm.status = str(status)
            await session.commit()
            return await self.get_by_id(task_id)

    async def add_stop(self, task_id: int, stop: TaskStop) -> Task:
        async with self.session() as session:
            session.add(TaskStopOrm(
                task_id=task_id,
                reason=stop.reason,
                stopped_at=stop.stopped_at,
                resumed_at=stop.resumed_at,
            ))
            orm = await session.get(TaskOrm, task_id)
            orm.status = str(TaskStatus.STOPPED)
            await session.commit()
            return await self.get_by_id(task_id)

    async def resume_stop(self, stop_id: int, resumed_at: datetime) -> None:
        async with self.session() as session:
            stop_orm = await session.get(TaskStopOrm, stop_id)
            stop_orm.resumed_at = resumed_at
            task_orm = await session.get(TaskOrm, stop_orm.task_id)
            task_orm.status = str(TaskStatus.IN_PROGRESS)
            await session.commit()

    async def delete(self, id: int) -> None:
        async with self.session() as session:
            orm = await session.get(TaskOrm, id)
            if orm:
                await session.delete(orm)
                await session.commit()
