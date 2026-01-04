import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models.attachment import Attachment, AttachmentCreate, AttachmentUpdate
from src.app.utils.naive_datetime import clean_model_datetimes


async def create_attachment(session: AsyncSession, attachment: AttachmentCreate) -> Attachment:
    data = attachment.model_dump()
    db_attachment = Attachment(**data)
    session.add(db_attachment)
    await session.commit()
    await session.refresh(db_attachment)
    return db_attachment


async def get_attachment(session: AsyncSession, attachment_id: uuid.UUID) -> Attachment | None:
    return await session.get(Attachment, attachment_id)


async def get_attachments(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Attachment]:
    result = await session.execute(select(Attachment).offset(skip).limit(limit))
    return result.scalars().all()


async def update_attachment(
    session: AsyncSession,
    attachment_id: uuid.UUID,
    attachment: AttachmentUpdate,
) -> Attachment | None:
    db_attachment = await session.get(Attachment, attachment_id)
    if db_attachment:
        update_data = attachment.model_dump(exclude_unset=True)
        clean_model_datetimes(update_data, ['created_at'])
        for key, value in update_data.items():
            setattr(db_attachment, key, value)
        await session.commit()
        await session.refresh(db_attachment)
    return db_attachment


async def delete_attachment(session: AsyncSession, attachment_id: uuid.UUID) -> Attachment | None:
    db_attachment = await session.get(Attachment, attachment_id)
    if db_attachment:
        await session.delete(db_attachment)
        await session.commit()
    return db_attachment
