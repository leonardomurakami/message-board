import random
import string
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


def generate_poster_id() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class PostBase(BaseModel):
    content: Optional[str] = None
    poster_id: Optional[str] = None
    image_path: Optional[str] = None


class PostCreate(PostBase):
    thread_id: int
    content: Optional[str] = None
    poster_id: Optional[str] = Field(default_factory=generate_poster_id)
    image_path: Optional[str] = None


class PostResponse(PostBase):
    id: int
    thread_id: int
    post_number: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
