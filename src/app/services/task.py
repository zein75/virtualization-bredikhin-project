import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud import task as crud_task
from src.app.db.models.task import TaskCreate, TaskPublic, TasksPublic, TaskUpdate


async def create_task_service(session: AsyncSession, task_in: TaskCreate) -> TaskPublic:
    task_in.due_at = task_in.due_at.replace(tzinfo=None) if task_in.due_at else None
    db_obj = await crud_task.create_task(session, task_in)
    return TaskPublic.model_validate(db_obj.model_dump())


async def get_task_service(session: AsyncSession, task_id: uuid.UUID) -> TaskPublic | None:
    db_obj = await crud_task.get_task(session, id=task_id)
    if db_obj is None:
        return None
    return TaskPublic.model_validate(db_obj.model_dump())


async def get_tasks_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> TasksPublic:
    db_objs = await crud_task.get_tasks(session, skip, limit)
    return TasksPublic.model_validate({
        'data': [TaskPublic.model_validate(obj.model_dump()) for obj in db_objs],
        'count': len(db_objs),
    })


async def update_task_service(
    session: AsyncSession, task_id: uuid.UUID, task_in: TaskUpdate,
) -> TaskPublic | None:
    task_in.due_at = task_in.due_at.replace(tzinfo=None) if task_in.due_at else None
    task_in.completed_at = (
        task_in.completed_at.replace(tzinfo=None) if task_in.completed_at else None
    )
    db_obj = await crud_task.update_task(session, task_id, task_in)
    if db_obj is None:
        return None
    return TaskPublic.model_validate(db_obj.model_dump())


async def delete_task_service(session: AsyncSession, task_id: uuid.UUID) -> TaskPublic | None:
    db_obj = await crud_task.delete_task(session, task_id)
    if db_obj is None:
        return None
    return TaskPublic.model_validate(db_obj.model_dump())
