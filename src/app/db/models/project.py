import datetime
import uuid

from sqlmodel import Field, SQLModel


class ProjectBase(SQLModel):
    name: str
    description: str | None = None
    color: str = Field(default='#9C9C9C')


class Project(ProjectBase, table=True):
    __tablename__ = 'projects'  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key='users.id', ondelete='CASCADE')
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.utcnow().replace(tzinfo=None),
    )


class ProjectCreate(ProjectBase):
    user_id: uuid.UUID


class ProjectUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    color: str | None = None

    def __init__(self, **data):
        super().__init__(**data)


class ProjectPublic(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime.datetime


class ProjectsPublic(SQLModel):
    data: list[ProjectPublic]
    count: int
