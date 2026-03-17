from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    thread_count = Column(Integer, default=0)

    # se deletar o board, deletar tambem todos os threads
    threads = relationship("Thread", back_populates="board", cascade="all, delete-orphan")
