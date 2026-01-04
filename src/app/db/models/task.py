import datetime
import uuid

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    title: str
    description: str | None = None


class Task(TaskBase, table=True):
    __tablename__ = 'tasks'  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID = Field(foreign_key='projects.id', ondelete='CASCADE')

    title: str
    description: str | None = None
    status: str
    priority: str

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now().replace(tzinfo=None),
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now().replace(tzinfo=None),
    )
    due_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None


class TaskCreate(TaskBase):
    project_id: uuid.UUID
    status: str
    priority: str
    due_at: datetime.datetime | None = None


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None


class TaskPublic(TaskBase):
    id: uuid.UUID
    project_id: uuid.UUID
    status: str
    priority: str
    due_at: datetime.datetime | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    completed_at: datetime.datetime | None = None


class TasksPublic(SQLModel):
    data: list[TaskPublic]
    count: int
