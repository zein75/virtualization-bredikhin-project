import datetime
import uuid

from sqlmodel import Field, SQLModel


class AttachmentBase(SQLModel):
    filename: str
    url: str
    content_type: str | None = None


class Attachment(AttachmentBase, table=True):
    __tablename__ = 'attachments'  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key='tasks.id', ondelete='CASCADE')

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now().replace(tzinfo=None),
    )


class AttachmentCreate(AttachmentBase):
    task_id: uuid.UUID


class AttachmentUpdate(SQLModel):
    filename: str | None = None
    url: str | None = None
    content_type: str | None = None

    def __init__(self, **data):
        super().__init__(**data)


class AttachmentPublic(AttachmentBase):
    id: uuid.UUID
    task_id: uuid.UUID
    created_at: datetime.datetime


class AttachmentsPublic(SQLModel):
    data: list[AttachmentPublic]
    count: int
