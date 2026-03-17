from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services import board_service

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("/")
def get_boards(db: Session = Depends(get_db)):
    return board_service.get_all_boards(db)


@router.get("/{board_id}")
def get_board(board_id: int, db: Session = Depends(get_db)):
    return board_service.get_board_by_id(db, board_id)
