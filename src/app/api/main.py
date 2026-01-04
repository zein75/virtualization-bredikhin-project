from fastapi import APIRouter

from src.app.api.routes import (
    attachment,
    healthcheck,
    login,
    project,
    tag,
    task,
    task_tag,
    users,
)

api_router = APIRouter()

api_router.include_router(
    users.router,
    tags=['users'],
    prefix='/users',
)
api_router.include_router(
    login.router,
    tags=['login'],
    prefix='/login',
)
api_router.include_router(
    healthcheck.router,
    tags=['healthcheck'],
)

api_router.include_router(
    attachment.router,
    tags=['attachments'],
    prefix='/attachments',
)
api_router.include_router(
    project.router,
    tags=['projects'],
    prefix='/projects',
)
api_router.include_router(
    tag.router,
    tags=['tags'],
    prefix='/tags',
)
api_router.include_router(
    task_tag.router,
    tags=['task_tags'],
    prefix='/task_tags',
)
api_router.include_router(
    task.router,
    tags=['tasks'],
    prefix='/tasks',
)
