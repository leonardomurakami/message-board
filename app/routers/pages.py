from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services import board_service, thread_service
from app.templates import templates

router = APIRouter(tags=["pages"])


@router.get("/", include_in_schema=False)
def home(request: Request, db: Session = Depends(get_db)):
    boards = board_service.get_popular_boards(db)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "猫-chan",
            "server_time": datetime.now(),
            "boards": boards,
        },
    )


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")


@router.get("/boards/{board_id}", include_in_schema=False)
def board_page(board_id: int, request: Request, db: Session = Depends(get_db)):
    board = board_service.get_board_by_id(db, board_id)
    if not board:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    threads = thread_service.get_all_threads(db, board_id)
    boards = board_service.get_popular_boards(db)  # for the header
    
    return templates.TemplateResponse(
        "board.html",
        {
            "request": request,
            "title": f"/{board.short_name}/ - {board.name}",
            "board": board,
            "threads": threads,
            "boards": boards,
        },
    )

