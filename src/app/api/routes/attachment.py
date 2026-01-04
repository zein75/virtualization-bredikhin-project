import uuid

from fastapi import APIRouter, HTTPException

from src.app.api.dependencies.common import SessionDep
from src.app.db.models.attachment import Attachment, AttachmentCreate, AttachmentUpdate
from src.app.services import attachment as attachment_service

router = APIRouter(prefix='/attachments', tags=['attachments'])


@router.post('/', response_model=Attachment)
async def create_attachment(attachment: AttachmentCreate, session: SessionDep) -> Attachment:
    return await attachment_service.create_attachment_service(session, attachment)


@router.get('/{attachment_id}', response_model=Attachment)
async def get_attachment(attachment_id: uuid.UUID, session: SessionDep) -> Attachment | None:
    db_attachment = await attachment_service.get_attachment_service(session, attachment_id)
    if db_attachment is None:
        raise HTTPException(status_code=404, detail='Attachment not found')
    return db_attachment


@router.get('/', response_model=list[Attachment])
async def get_attachments(session: SessionDep, skip: int = 0, limit: int = 100):
    return await attachment_service.get_attachments_service(session, skip, limit)


@router.put('/{attachment_id}', response_model=Attachment)
async def update_attachment(
    attachment_id: uuid.UUID, attachment: AttachmentUpdate, session: SessionDep,
):
    db_attachment = await attachment_service.update_attachment_service(
        session, attachment_id, attachment,
    )
    if db_attachment is None:
        raise HTTPException(status_code=404, detail='Attachment not found')
    return db_attachment


@router.delete('/{attachment_id}', response_model=Attachment)
async def delete_attachment(attachment_id: uuid.UUID, session: SessionDep):
    db_attachment = await attachment_service.delete_attachment_service(session, attachment_id)
    if db_attachment is None:
        raise HTTPException(status_code=404, detail='Attachment not found')
    return db_attachment
