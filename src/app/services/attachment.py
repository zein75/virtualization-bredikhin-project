import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud import attachment as crud_attachment
from src.app.db.models.attachment import (
    AttachmentCreate,
    AttachmentPublic,
    AttachmentUpdate,
)


async def create_attachment_service(
    session: AsyncSession,
    attachment: AttachmentCreate,
) -> AttachmentPublic:
    db_obj = await crud_attachment.create_attachment(session, attachment)
    return AttachmentPublic.model_validate(db_obj.model_dump())

async def get_attachment_service(
    session: AsyncSession,
    attachment_id: uuid.UUID,
) -> AttachmentPublic | None:
    db_obj = await crud_attachment.get_attachment(session, attachment_id)
    if db_obj is None:
        return None
    return AttachmentPublic.model_validate(db_obj.model_dump())

async def get_attachments_service(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[AttachmentPublic]:
    db_objs = await crud_attachment.get_attachments(session, skip, limit)
    return [AttachmentPublic.model_validate(obj.model_dump()) for obj in db_objs]

async def update_attachment_service(
    session: AsyncSession,
    attachment_id: uuid.UUID,
    attachment: AttachmentUpdate,
) -> AttachmentPublic | None:
    db_obj = await crud_attachment.update_attachment(session, attachment_id, attachment)
    if db_obj is None:
        return None
    return AttachmentPublic.model_validate(db_obj.model_dump())

async def delete_attachment_service(
    session: AsyncSession,
    attachment_id: uuid.UUID,
) -> AttachmentPublic | None:
    db_obj = await crud_attachment.delete_attachment(session, attachment_id)
    if db_obj is None:
        return None
    return AttachmentPublic.model_validate(db_obj.model_dump())
