import datetime
import uuid

from sqlmodel import Field, SQLModel


class TagBase(SQLModel):
    name: str


class Tag(TagBase, table=True):
    __tablename__ = 'tags'  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key='users.id', ondelete='CASCADE')
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now().replace(tzinfo=None),
    )


class TagCreate(TagBase):
    user_id: uuid.UUID


class TagUpdate(SQLModel):
    name: str | None = None

    def __init__(self, **data):
        super().__init__(**data)


class TagPublic(TagBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime.datetime


class TagsPublic(SQLModel):
    data: list[TagPublic]
    count: int
