from sqlalchemy.orm import Session

from app.models.thread import Thread


def get_all_threads(db: Session, board_id: int = None) -> list[Thread]:
    query = db.query(Thread)
    if board_id:
        query = query.filter(Thread.board_id == board_id)
    return query.all()


def get_thread_by_id(db: Session, thread_id: int) -> Thread | None:
    return db.query(Thread).filter(Thread.id == thread_id).first()
