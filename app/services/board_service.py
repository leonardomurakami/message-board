from sqlalchemy.orm import Session

from app.models.board import Board
from app.schemas.board import BoardCreate


def get_all_boards(db: Session) -> list[Board]:
    query = db.query(Board).all()
    db.commit()
    return query


def get_board_by_id(db: Session, board_id: int) -> Board | None:
    query = db.query(Board).filter(Board.id == board_id).first()
    db.commit()
    return query


def get_popular_boards(db: Session, limit: int = 10) -> list[Board]:
    query = db.query(Board).order_by(Board.thread_count.desc()).limit(limit).all()
    db.commit()
    return query


def create_board(db: Session, board: BoardCreate) -> Board:
    db_board = Board(
        short_name=board.short_name,
        name=board.name,
        description=board.description,
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board
