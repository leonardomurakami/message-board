from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.database import Base


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    bumped_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    post_count = Column(Integer, default=0)
    image_count = Column(Integer, default=0)

    board = relationship("Board", back_populates="threads")
    # se deletar o thread, deletar tambem todos os posts associados
    posts = relationship("Post", back_populates="thread", cascade="all, delete-orphan")
