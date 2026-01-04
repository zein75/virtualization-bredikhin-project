import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models.project import Project, ProjectCreate, ProjectUpdate
from src.app.utils.naive_datetime import clean_model_datetimes


async def create_project(session: AsyncSession, project: ProjectCreate) -> Project:
    data = project.model_dump()
    clean_model_datetimes(data, ['created_at'])
    db_project = Project(**data)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project(session: AsyncSession, project_id: uuid.UUID) -> Project | None:
    return await session.get(Project, project_id)


async def get_projects(session: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Project]:
    result = await session.execute(select(Project).offset(skip).limit(limit))
    return result.scalars().all()


async def update_project(
    session: AsyncSession,
    project_id: uuid.UUID,
    project: ProjectUpdate,
) -> Project | None:
    db_project = await session.get(Project, project_id)
    if db_project:
        update_data = project.model_dump(exclude_unset=True)
        clean_model_datetimes(update_data, ['created_at'])
        for key, value in update_data.items():
            setattr(db_project, key, value)
        await session.commit()
        await session.refresh(db_project)
    return db_project


async def delete_project(session: AsyncSession, project_id: uuid.UUID) -> Project | None:
    db_project = await session.get(Project, project_id)
    if db_project:
        await session.delete(db_project)
        await session.commit()
    return db_project
