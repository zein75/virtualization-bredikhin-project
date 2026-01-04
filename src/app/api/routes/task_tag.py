import uuid

from fastapi import APIRouter, HTTPException

from src.app.api.dependencies.common import SessionDep
from src.app.db.models.task_tag import TaskTag, TaskTagCreate, TaskTagUpdate
from src.app.services import task_tag as task_tag_service

router = APIRouter(prefix='/task_tags', tags=['task_tags'])


@router.post('/', response_model=TaskTag)
async def create_task_tag(task_tag: TaskTagCreate, session: SessionDep) -> TaskTag:
    return await task_tag_service.create_task_tag_service(session, task_tag)


@router.get('/{task_tag_id}', response_model=TaskTag)
async def get_task_tag(task_tag_id: uuid.UUID, session: SessionDep) -> TaskTag | None:
    db_task_tag = await task_tag_service.get_task_tag_service(session, task_tag_id)
    if db_task_tag is None:
        raise HTTPException(status_code=404, detail='TaskTag not found')
    return db_task_tag


@router.get('/', response_model=list[TaskTag])
async def get_task_tags(session: SessionDep, skip: int = 0, limit: int = 100):
    return await task_tag_service.get_task_tags_service(session, skip, limit)


@router.put('/{task_tag_id}', response_model=TaskTag)
async def update_task_tag(task_tag_id: uuid.UUID, task_tag: TaskTagUpdate, session: SessionDep):
    db_task_tag = await task_tag_service.update_task_tag_service(session, task_tag_id, task_tag)
    if db_task_tag is None:
        raise HTTPException(status_code=404, detail='TaskTag not found')
    return db_task_tag


@router.delete('/{task_tag_id}', response_model=TaskTag)
async def delete_task_tag(task_tag_id: uuid.UUID, session: SessionDep):
    db_task_tag = await task_tag_service.delete_task_tag_service(session, task_tag_id)
    if db_task_tag is None:
        raise HTTPException(status_code=404, detail='TaskTag not found')
    return db_task_tag
