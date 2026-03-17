from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate


def get_all_threads(db: Session, board_id: int = None) -> list[Thread]:
    query = db.query(Thread)
    if board_id:
        query = query.filter(Thread.board_id == board_id)
    return query.all()


def get_thread_by_id(db: Session, thread_id: int) -> Thread | None:
    return db.query(Thread).filter(Thread.id == thread_id).first()


def create_thread(db: Session, board_id: int, thread: ThreadCreate) -> Thread:
    db_thread = Thread(
        board_id=board_id,
        title=thread.title,
    )
    db.add(db_thread)
    
    board = db.query(Board).filter(Board.id == board_id).first()
    if board:
        board.thread_count += 1
        
    db.commit()
    db.refresh(db_thread)
    return db_thread
