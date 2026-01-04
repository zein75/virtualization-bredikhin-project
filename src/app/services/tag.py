import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud import tag as crud_tag
from src.app.db.models.tag import TagCreate, TagPublic, TagsPublic, TagUpdate


async def create_tag_service(session: AsyncSession, tag: TagCreate) -> TagPublic:
    db_obj = await crud_tag.create_tag(session, tag)
    return TagPublic.model_validate(db_obj.model_dump())

async def get_tag_service(session: AsyncSession, tag_id: uuid.UUID) -> TagPublic | None:
    db_obj = await crud_tag.get_tag(session, tag_id)
    if db_obj is None:
        return None
    return TagPublic.model_validate(db_obj.model_dump())

async def get_tags_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> TagsPublic:
    db_objs = await crud_tag.get_tags(session, skip, limit)
    return TagsPublic.model_validate({
        "data": [TagPublic.model_validate(obj.model_dump()) for obj in db_objs],
        "count": len(db_objs),
    })

async def update_tag_service(
    session: AsyncSession,
    tag_id: uuid.UUID,
    tag: TagUpdate,
) -> TagPublic | None:
    db_obj = await crud_tag.update_tag(session, tag_id, tag)
    if db_obj is None:
        return None
    return TagPublic.model_validate(db_obj.model_dump())

async def delete_tag_service(session: AsyncSession, tag_id: uuid.UUID) -> TagPublic | None:
    db_obj = await crud_tag.delete_tag(session, tag_id)
    if db_obj is None:
        return None
    return TagPublic.model_validate(db_obj.model_dump())
