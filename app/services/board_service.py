from sqlalchemy.orm import Session

from app.models.board import Board


def get_all_boards(db: Session) -> list[Board]:
    return db.query(Board).all()


def get_board_by_id(db: Session, board_id: int) -> Board | None:
    return db.query(Board).filter(Board.id == board_id).first()
