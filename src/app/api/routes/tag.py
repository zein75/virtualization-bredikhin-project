import uuid

from fastapi import APIRouter, HTTPException

from src.app.api.dependencies.common import SessionDep
from src.app.db.models.tag import TagCreate, TagPublic, TagsPublic, TagUpdate
from src.app.services import tag as tag_service

router = APIRouter(prefix='/tags', tags=['tags'])


@router.post('/', response_model=TagPublic)
async def create_tag(tag: TagCreate, session: SessionDep) -> TagPublic:
    return await tag_service.create_tag_service(session, tag)


@router.get('/{tag_id}', response_model=TagPublic)
async def get_tag(tag_id: uuid.UUID, session: SessionDep) -> TagPublic | None:
    db_tag = await tag_service.get_tag_service(session, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail='Tag not found')
    return db_tag


@router.get('/', response_model=TagsPublic)
async def get_tags(session: SessionDep, skip: int = 0, limit: int = 100):
    return await tag_service.get_tags_service(session, skip, limit)


@router.put('/{tag_id}', response_model=TagPublic)
async def update_tag(tag_id: uuid.UUID, tag: TagUpdate, session: SessionDep):
    db_tag = await tag_service.update_tag_service(session, tag_id, tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail='Tag not found')
    return db_tag


@router.delete('/{tag_id}', response_model=TagPublic)
async def delete_tag(tag_id: uuid.UUID, session: SessionDep):
    db_tag = await tag_service.delete_tag_service(session, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail='Tag not found')
    return db_tag
