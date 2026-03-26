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

# board creation should be behind a secure admin panel or something like that
# i will not invest much time into this seeing as it is not the main focus of the project
# this works for now


class BoardResponse(BoardBase):
    id: int
    thread_count: int

    model_config = ConfigDict(from_attributes=True)
