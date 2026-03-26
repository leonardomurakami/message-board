from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ThreadBase(BaseModel):
    title: str


class ThreadCreate(ThreadBase):
    content: str | None = None


class ThreadResponse(ThreadBase):
    id: int
    board_id: int
    created_at: datetime
    bumped_at: datetime
    post_count: int
    image_count: int

    model_config = ConfigDict(from_attributes=True)
