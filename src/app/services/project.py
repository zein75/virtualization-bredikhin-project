import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud import project as crud_project
from src.app.db.models.project import ProjectCreate, ProjectPublic, ProjectsPublic, ProjectUpdate


async def create_project_service(session: AsyncSession, project: ProjectCreate) -> ProjectPublic:
    db_obj = await crud_project.create_project(session, project)
    return ProjectPublic.model_validate(db_obj.model_dump())

async def get_project_service(session: AsyncSession, project_id: uuid.UUID) -> ProjectPublic | None:
    db_obj = await crud_project.get_project(session, project_id)
    if db_obj is None:
        return None
    return ProjectPublic.model_validate(db_obj.model_dump())

async def get_projects_service(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> ProjectsPublic:
    db_objs = await crud_project.get_projects(session, skip, limit)
    return ProjectsPublic.model_validate({
        "data": [ProjectPublic.model_validate(obj.model_dump()) for obj in db_objs],
        "count": len(db_objs),
    })

async def update_project_service(
    session: AsyncSession,
    project_id: uuid.UUID,
    project: ProjectUpdate,
) -> ProjectPublic | None:
    db_obj = await crud_project.update_project(session, project_id, project)
    if db_obj is None:
        return None
    return ProjectPublic.model_validate(db_obj.model_dump())

async def delete_project_service(
    session: AsyncSession,
    project_id: uuid.UUID,
) -> ProjectPublic | None:
    db_obj = await crud_project.delete_project(session, project_id)
    if db_obj is None:
        return None
    return ProjectPublic.model_validate(db_obj.model_dump())
