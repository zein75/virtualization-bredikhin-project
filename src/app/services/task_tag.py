import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud import task_tag as crud_task_tag
from src.app.db.models.task_tag import TaskTag, TaskTagCreate, TaskTagUpdate


async def create_task_tag_service(session: AsyncSession, task_tag: TaskTagCreate) -> TaskTag:
    db_obj = await crud_task_tag.create_task_tag(session, task_tag)
    return TaskTag.model_validate(db_obj.model_dump())

async def get_task_tag_service(session: AsyncSession, task_tag_id: uuid.UUID) -> TaskTag | None:
    db_obj = await crud_task_tag.get_task_tag(session, task_tag_id)
    if db_obj is None:
        return None
    return TaskTag.model_validate(db_obj.model_dump())

async def get_task_tags_service(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[TaskTag]:
    db_objs = await crud_task_tag.get_task_tags(session, skip, limit)
    return [TaskTag.model_validate(obj.model_dump()) for obj in db_objs]

async def update_task_tag_service(
    session: AsyncSession,
    task_tag_id: uuid.UUID,
    task_tag: TaskTagUpdate,
) -> TaskTag | None:
    db_obj = await crud_task_tag.update_task_tag(session, task_tag_id, task_tag)
    if db_obj is None:
        return None
    return TaskTag.model_validate(db_obj.model_dump())

async def delete_task_tag_service(session: AsyncSession, task_tag_id: uuid.UUID) -> TaskTag | None:
    db_obj = await crud_task_tag.delete_task_tag(session, task_tag_id)
    if db_obj is None:
        return None
    return TaskTag.model_validate(db_obj.model_dump())
