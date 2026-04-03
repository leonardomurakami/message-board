import math
from datetime import UTC, datetime

from sqlalchemy.orm import Session, joinedload

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


def get_trending_threads(
    db: Session, limit: int = 12, candidate_pool: int = 200
) -> list[tuple[Thread, Post | None]]:
    now = datetime.now(UTC)
    candidates = (
        db.query(Thread)
        .options(joinedload(Thread.board))
        .filter(Thread.post_count > 0)
        .order_by(Thread.bumped_at.desc())
        .limit(candidate_pool)
        .all()
    )

    def how_hot(t: Thread) -> float:
        bumped = t.bumped_at
        if bumped is None:
            return 0.0
        if bumped.tzinfo is None:
            bumped = bumped.replace(tzinfo=UTC)
        hours = max((now - bumped).total_seconds() / 3600.0, 0.25)
        return t.post_count / math.sqrt(hours)

    candidates.sort(key=how_hot, reverse=True)
    threads = candidates[:limit]

    if not threads:
        return []

    ids = [t.id for t in threads]
    posts = (
        db.query(Post)
        .filter(Post.thread_id.in_(ids))
        .order_by(Post.thread_id.asc(), Post.post_number.asc())
        .all()
    )
    first_by_tid: dict[int, Post] = {}
    for p in posts:
        if p.thread_id not in first_by_tid:
            first_by_tid[p.thread_id] = p

    return [(t, first_by_tid.get(t.id)) for t in threads]


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
