import datetime

from pydantic import BaseModel, Field


class Image(BaseModel):
    id: int | None = Field(default=None)
    filePath: str = Field(alias="file_path")
    createdAt: datetime.datetime | None = Field(default=None, alias="created_at")