from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.thread import ThreadCreate, ThreadResponse
from app.services import thread_service

router = APIRouter(prefix="/threads", tags=["threads"])


@router.get("/")
def get_threads(board_id: int = None, db: Session = Depends(get_db)):
    return thread_service.get_all_threads(db, board_id)


@router.get("/{thread_id}")
def get_thread(thread_id: int, db: Session = Depends(get_db)):
    return thread_service.get_thread_by_id(db, thread_id)


@router.post("/", response_model=ThreadResponse)
def create_thread(board_id: int, thread: ThreadCreate, db: Session = Depends(get_db)):
    return thread_service.create_thread(db, board_id, thread)
