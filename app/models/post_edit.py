from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class PostEdit(Base):
    __tablename__ = "post_edits"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    old_content = Column(Text, nullable=True)
    edited_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    post = relationship("Post", back_populates="edits")
