from sqlmodel import SQLModel


class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class FilePath(SQLModel):
    file_path: str


class FileUploadResponse(SQLModel):
    object_key: str
    file_url: str
