import uuid

from sqlmodel import Field, SQLModel


class TaskTag(SQLModel, table=True):
    __tablename__ = 'task_tag'  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(
        default=None,
        foreign_key='tasks.id',
        primary_key=True,
        ondelete='CASCADE',
    )
    tag_id: uuid.UUID = Field(
        default=None,
        foreign_key='tags.id',
        primary_key=True,
        ondelete='CASCADE',
    )


class TaskTagCreate(SQLModel):
    task_id: uuid.UUID
    tag_id: uuid.UUID


class TaskTagUpdate(SQLModel):
    task_id: uuid.UUID | None = None
    tag_id: uuid.UUID | None = None
