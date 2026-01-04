import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models.tag import Tag, TagCreate, TagUpdate
from src.app.utils.naive_datetime import clean_model_datetimes


async def create_tag(session: AsyncSession, tag: TagCreate) -> Tag:
    data = tag.model_dump()
    clean_model_datetimes(data, ['created_at'])
    db_tag = Tag(**data)
    session.add(db_tag)
    await session.commit()
    await session.refresh(db_tag)
    return db_tag


async def get_tag(session: AsyncSession, tag_id: uuid.UUID) -> Tag | None:
    return await session.get(Tag, tag_id)


async def get_tags(session: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Tag]:
    result = await session.execute(select(Tag).offset(skip).limit(limit))
    return result.scalars().all()


async def update_tag(session: AsyncSession, tag_id: uuid.UUID, tag: TagUpdate) -> Tag | None:
    db_tag = await session.get(Tag, tag_id)
    if db_tag:
        update_data = tag.model_dump(exclude_unset=True)
        clean_model_datetimes(update_data, ['created_at'])
        for key, value in update_data.items():
            setattr(db_tag, key, value)
        await session.commit()
        await session.refresh(db_tag)
    return db_tag


async def delete_tag(session: AsyncSession, tag_id: uuid.UUID) -> Tag | None:
    db_tag = await session.get(Tag, tag_id)
    if db_tag:
        await session.delete(db_tag)
        await session.commit()
    return db_tag
