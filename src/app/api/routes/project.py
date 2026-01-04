import uuid

from fastapi import APIRouter, HTTPException

from src.app.api.dependencies.common import SessionDep
from src.app.db.models.project import (
    ProjectCreate,
    ProjectPublic,
    ProjectsPublic,
    ProjectUpdate,
)
from src.app.services import project as project_service

router = APIRouter(prefix='/projects', tags=['projects'])


@router.post('/', response_model=ProjectPublic)
async def create_project(project: ProjectCreate, session: SessionDep) -> ProjectPublic:
    return await project_service.create_project_service(session, project)


@router.get('/{project_id}', response_model=ProjectPublic)
async def get_project(project_id: uuid.UUID, session: SessionDep) -> ProjectPublic | None:
    db_project = await project_service.get_project_service(session, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    return db_project


@router.get('/', response_model=ProjectsPublic)
async def get_projects(session: SessionDep, skip: int = 0, limit: int = 100):
    return await project_service.get_projects_service(session, skip, limit)


@router.put('/{project_id}', response_model=ProjectPublic)
async def update_project(project_id: uuid.UUID, project: ProjectUpdate, session: SessionDep):
    db_project = await project_service.update_project_service(session, project_id, project)
    if db_project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    return db_project


@router.delete('/{project_id}', response_model=ProjectPublic)
async def delete_project(project_id: uuid.UUID, session: SessionDep):
    db_project = await project_service.delete_project_service(session, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    return db_project
