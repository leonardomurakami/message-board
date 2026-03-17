from typing import Optional

from pydantic import BaseModel, ConfigDict, validator


class BoardBase(BaseModel):
    short_name: str
    name: str
    description: Optional[str] = None

    @validator("short_name")
    def validate_short_name(cls, v):
        if not v.islower():
            raise ValueError("Short name must be lowercase")
        if len(v) > 3:
            raise ValueError("Short name must be at most 3 characters long")
        return v


class BoardCreate(BoardBase):
    pass


class BoardResponse(BoardBase):
    id: int
    thread_count: int

    model_config = ConfigDict(from_attributes=True)
