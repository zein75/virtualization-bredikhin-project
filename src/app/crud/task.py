import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models.task import Task, TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, task_in: TaskCreate) -> Task:
    data = task_in.model_dump()
    db_task = Task(**data)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_task(db: AsyncSession, **filters) -> Task | None:
    return await db.get(Task, filters)


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Task]:
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()


async def update_task(db: AsyncSession, task_id: uuid.UUID, task: TaskUpdate) -> Task | None:
    db_task = await db.get(Task, task_id)
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: uuid.UUID) -> Task | None:
    db_task = await db.get(Task, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task
