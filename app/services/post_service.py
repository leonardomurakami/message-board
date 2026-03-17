from sqlalchemy.orm import Session

from app.models.post import Post


def get_all_posts(db: Session, thread_id: int = None) -> list[Post]:
    query = db.query(Post)
    if thread_id:
        query = query.filter(Post.thread_id == thread_id)
    return query.all()


def get_post_by_id(db: Session, post_id: int) -> Post | None:
    return db.query(Post).filter(Post.id == post_id).first()
