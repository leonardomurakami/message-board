from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    content: Optional[str] = None
    poster_id: Optional[str] = None
    image_path: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    thread_id: int
    post_number: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
