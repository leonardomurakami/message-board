from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
def get_posts(thread_id: int = None, db: Session = Depends(get_db)):
    return post_service.get_all_posts(db, thread_id)


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_post_by_id(db, post_id)
