import uuid

from fastapi import APIRouter, HTTPException

from src.app.api.dependencies.common import SessionDep
from src.app.db.models.task import TaskCreate, TaskPublic, TasksPublic, TaskUpdate
from src.app.services import task as task_service

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', response_model=TaskPublic)
async def create_task(task: TaskCreate, session: SessionDep) -> TaskPublic:
    return await task_service.create_task_service(session, task)


@router.get('/{task_id}', response_model=TaskPublic)
async def get_task(task_id: uuid.UUID, session: SessionDep) -> TaskPublic | None:
    db_task = await task_service.get_task_service(session, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return db_task


@router.get('/', response_model=TasksPublic)
async def get_tasks(session: SessionDep, skip: int = 0, limit: int = 100):
    return await task_service.get_tasks_service(session, skip, limit)


@router.put('/{task_id}', response_model=TaskPublic)
async def update_task(task_id: uuid.UUID, task: TaskUpdate, session: SessionDep):
    db_task = await task_service.update_task_service(session, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return db_task


@router.delete('/{task_id}', response_model=TaskPublic)
async def delete_task(task_id: uuid.UUID, session: SessionDep):
    db_task = await task_service.delete_task_service(session, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return db_task
