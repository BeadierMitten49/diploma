from datetime import datetime

from src.domain.employee import Permission
from src.domain.exceptions import InvalidTaskStatusError, EmployeePermissionError
from src.domain.task import Task, TaskStatus, TaskStop
from src.infrastructure.database.repositories.task import TaskRepository


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def get_tasks(self) -> list[Task]:
        return await self.task_repo.get_all()

    async def get_task(self, id: int) -> Task | None:
        return await self.task_repo.get_by_id(id)

    async def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        return await self.task_repo.get_by_status(status)

    async def create_task(self, task: Task) -> Task:
        if Permission.TASKS not in task.employee.role.permissions:
            raise EmployeePermissionError(
                f"Сотрудник «{task.employee.name}» не имеет доступа к задачам производства"
            )
        return await self.task_repo.create(task)

    async def start_task(self, task_id: int) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if task.status != TaskStatus.PENDING:
            raise InvalidTaskStatusError(f"Нельзя начать задачу со статусом «{task.status}»")
        return await self.task_repo.update_status(task_id, TaskStatus.IN_PROGRESS)

    async def stop_task(self, task_id: int, reason: str) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if task.status != TaskStatus.IN_PROGRESS:
            raise InvalidTaskStatusError(f"Нельзя остановить задачу со статусом «{task.status}»")
        stop = TaskStop(reason=reason, stopped_at=datetime.now())
        return await self.task_repo.add_stop(task_id, stop)

    async def resume_task(self, task_id: int) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if task.status != TaskStatus.STOPPED:
            raise InvalidTaskStatusError(f"Нельзя возобновить задачу со статусом «{task.status}»")
        last_stop = next((s for s in reversed(task.stops) if s.resumed_at is None), None)
        if last_stop:
            await self.task_repo.resume_stop(last_stop.id, datetime.now())
        return await self.task_repo.get_by_id(task_id)

    async def delete_task(self, id: int) -> None:
        await self.task_repo.delete(id)
