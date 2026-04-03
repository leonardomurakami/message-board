from datetime import UTC, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.post import Post
from app.models.post_edit import PostEdit
from app.models.thread import Thread
from app.schemas.post import PostCreate


def get_all_posts(
    db: Session, thread_id: int = None, limit: int = None, offset: int = None
) -> list[Post]:
    query = db.query(Post).order_by(Post.post_number.asc())
    if thread_id:
        query = query.filter(Post.thread_id == thread_id)
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    return query.all()


def get_post_count(db: Session, thread_id: int = None) -> int:
    query = db.query(Post)
    if thread_id:
        query = query.filter(Post.thread_id == thread_id)
    return query.count()


def get_post_by_id(db: Session, post_id: int) -> Post | None:
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, thread_id: int, post: PostCreate) -> Post:
    thread = db.query(Thread).filter(Thread.id == thread_id).first()

    max_post_num = db.query(func.max(Post.post_number)).filter(Post.thread_id == thread_id).scalar()
    post_number = (max_post_num or 0) + 1

    db_post = Post(
        thread_id=thread_id,
        post_number=post_number,
        content=post.content,
        poster_id=post.poster_id,
        owner=post.owner,
        image_path=post.image_path,
    )
    db.add(db_post)

    if thread:
        thread.post_count += 1
        thread.bumped_at = datetime.now(UTC)
        if post.image_path:
            thread.image_count += 1

    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> dict:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"deleted": False}

    thread_id = post.thread_id
    thread = db.query(Thread).filter(Thread.id == thread_id).first()

    db.delete(post)

    thread_deleted = False
    board_id = None
    if thread:
        thread.post_count = max(thread.post_count - 1, 0)
        remaining = db.query(Post).filter(Post.thread_id == thread_id, Post.id != post_id).count()
        if remaining == 0:
            board = db.query(Board).filter(Board.id == thread.board_id).first()
            if board:
                board.thread_count = max(board.thread_count - 1, 0)
                board_id = board.id
            db.delete(thread)
            thread_deleted = True

    db.commit()
    return {"deleted": True, "thread_deleted": thread_deleted, "board_id": board_id}


def update_post_content(db: Session, post_id: int, content: str) -> Post | None:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None

    edit = PostEdit(
        post_id=post.id,
        old_content=post.content,
    )
    db.add(edit)

    post.content = content
    post.edited_at = datetime.now(UTC)
    db.commit()
    db.refresh(post)
    return post


def get_post_edits(db: Session, post_id: int) -> list[PostEdit]:
    return (
        db.query(PostEdit)
        .filter(PostEdit.post_id == post_id)
        .order_by(PostEdit.edited_at.desc())
        .all()
    )
