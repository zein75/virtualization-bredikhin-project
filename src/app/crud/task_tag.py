import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models.task_tag import TaskTag, TaskTagCreate, TaskTagUpdate


async def create_task_tag(session: AsyncSession, task_tag: TaskTagCreate) -> TaskTag:
    db_task_tag = TaskTag(**task_tag.model_dump())
    session.add(db_task_tag)
    await session.commit()
    await session.refresh(db_task_tag)
    return db_task_tag

async def get_task_tag(session: AsyncSession, task_tag_id: uuid.UUID) -> TaskTag | None:
    return await session.get(TaskTag, task_tag_id)

async def get_task_tags(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[TaskTag]:
    result = await session.execute(select(TaskTag).offset(skip).limit(limit))
    return result.scalars().all()

async def update_task_tag(
    session: AsyncSession,
    task_tag_id: uuid.UUID,
    task_tag: TaskTagUpdate,
) -> TaskTag | None:
    db_task_tag = await session.get(TaskTag, task_tag_id)
    if db_task_tag:
        for key, value in task_tag.model_dump(exclude_unset=True).items():
            setattr(db_task_tag, key, value)
        await session.commit()
        await session.refresh(db_task_tag)
    return db_task_tag

async def delete_task_tag(session: AsyncSession, task_tag_id: uuid.UUID) -> TaskTag | None:
    db_task_tag = await session.get(TaskTag, task_tag_id)
    if db_task_tag:
        await session.delete(db_task_tag)
        await session.commit()
    return db_task_tag
