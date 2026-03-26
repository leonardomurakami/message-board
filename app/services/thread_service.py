from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.post import Post
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate
from app.schemas.post import generate_poster_id


def get_all_threads(
    db: Session, board_id: int = None, limit: int = None, offset: int = None
) -> list[Thread]:
    query = db.query(Thread).order_by(Thread.bumped_at.desc())
    if board_id:
        query = query.filter(Thread.board_id == board_id)
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    return query.all()


def get_thread_count(db: Session, board_id: int = None) -> int:
    query = db.query(Thread)
    if board_id:
        query = query.filter(Thread.board_id == board_id)
    return query.count()


def get_thread_by_id(db: Session, thread_id: int) -> Thread | None:
    return db.query(Thread).filter(Thread.id == thread_id).first()


def create_thread(db: Session, board_id: int, thread: ThreadCreate) -> Thread:
    db_thread = Thread(
        board_id=board_id,
        title=thread.title,
    )
    db.add(db_thread)
    db.flush()

    if thread.content:
        db_post = Post(
            thread_id=db_thread.id,
            content=thread.content,
            post_number=1,
            poster_id=generate_poster_id(),
        )
        db.add(db_post)
        db_thread.post_count += 1

    board = db.query(Board).filter(Board.id == board_id).first()
    if board:
        board.thread_count += 1

    db.commit()
    db.refresh(db_thread)
    return db_thread
