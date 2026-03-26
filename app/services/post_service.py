from datetime import UTC, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.post import Post
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
