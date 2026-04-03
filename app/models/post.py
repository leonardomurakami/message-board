from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)
    post_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    poster_id = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    edited_at = Column(DateTime(timezone=True), nullable=True)

    thread = relationship("Thread", back_populates="posts")
    edits = relationship("PostEdit", back_populates="post", cascade="all, delete-orphan", order_by="PostEdit.edited_at.desc()")
