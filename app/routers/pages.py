from datetime import datetime

from fastapi import APIRouter, Cookie, Depends, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.post import PostCreate
from app.schemas.thread import ThreadCreate
from app.services import board_service, post_service, thread_service
from app.templates import templates

router = APIRouter(tags=["pages"])


def _get_logged_user(request: Request) -> str | None:
    return request.cookies.get("mb_user") or None


@router.get("/", include_in_schema=False)
def home(request: Request, db: Session = Depends(get_db)):
    boards = board_service.get_popular_boards(db)
    all_boards = sorted(
        board_service.get_all_boards(db),
        key=lambda b: (b.short_name.lower(), b.id),
    )
    trending = thread_service.get_trending_threads(db, limit=15)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "猫-chan",
            "server_time": datetime.now(),
            "boards": boards,
            "all_boards": all_boards,
            "trending_threads": trending,
            "logged_user": _get_logged_user(request),
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

    limit = 10
    threads = thread_service.get_all_threads(db, board_id, limit=limit, offset=0)
    total_thread_count = thread_service.get_thread_count(db, board_id)
    boards = board_service.get_popular_boards(db)  # for the header

    return templates.TemplateResponse(
        "board.html",
        {
            "request": request,
            "title": f"/{board.short_name}/ - {board.name}",
            "board": board,
            "threads": threads,
            "boards": boards,
            "total_thread_count": total_thread_count,
            "limit": limit,
            "logged_user": _get_logged_user(request),
        },
    )


@router.get("/threads/{thread_id}", include_in_schema=False)
def thread_page(thread_id: int, request: Request, db: Session = Depends(get_db)):
    thread = thread_service.get_thread_by_id(db, thread_id)
    if not thread:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    board = board_service.get_board_by_id(db, thread.board_id)
    if not board:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    posts = post_service.get_all_posts(db, thread_id)
    boards = board_service.get_popular_boards(db)

    return templates.TemplateResponse(
        "thread.html",
        {
            "request": request,
            "title": f"/{board.short_name}/ - {thread.title}",
            "board": board,
            "thread": thread,
            "posts": posts,
            "boards": boards,
            "logged_user": _get_logged_user(request),
        },
    )


@router.post("/pages/boards/{board_id}/threads", include_in_schema=False)
def create_thread_htmx(
    board_id: int,
    request: Request,
    title: str = Form(...),
    content: str = Form(None),
    db: Session = Depends(get_db),
):
    owner = _get_logged_user(request)
    if not owner:
        return HTMLResponse("Login required", status_code=403)
    thread_data = ThreadCreate(title=title, content=content)
    new_thread = thread_service.create_thread(db, board_id, thread_data, owner=owner)

    return templates.TemplateResponse(
        "components/thread_preview.html", {"request": request, "thread": new_thread, "logged_user": owner}
    )


@router.get("/pages/threads/{thread_id}/expand", include_in_schema=False)
def expand_thread_htmx(thread_id: int, request: Request, db: Session = Depends(get_db)):
    thread = thread_service.get_thread_by_id(db, thread_id)
    limit = 10
    posts = post_service.get_all_posts(db, thread_id, limit=limit, offset=0)
    total_post_count = post_service.get_post_count(db, thread_id)
    return templates.TemplateResponse(
        "components/thread_expanded.html",
        {
            "request": request,
            "thread": thread,
            "posts": posts,
            "total_post_count": total_post_count,
            "limit": limit,
            "logged_user": _get_logged_user(request),
        },
    )


@router.get("/pages/threads/{thread_id}/collapse", include_in_schema=False)
def collapse_thread_htmx(thread_id: int, request: Request, db: Session = Depends(get_db)):
    thread = thread_service.get_thread_by_id(db, thread_id)
    return templates.TemplateResponse(
        "components/thread_preview.html", {"request": request, "thread": thread, "logged_user": _get_logged_user(request)}
    )


@router.post("/pages/threads/{thread_id}/posts", include_in_schema=False)
def create_post_htmx(
    thread_id: int, request: Request, content: str = Form(None), db: Session = Depends(get_db)
):
    owner = _get_logged_user(request)
    if not owner:
        return HTMLResponse("Login required", status_code=403)
    post_data = PostCreate(content=content, thread_id=thread_id, owner=owner)
    new_post = post_service.create_post(db, thread_id, post_data)

    return templates.TemplateResponse(
        "components/post.html", {"request": request, "post": new_post, "logged_user": owner}
    )


@router.delete("/pages/posts/{post_id}", include_in_schema=False)
def delete_post_htmx(post_id: int, request: Request, db: Session = Depends(get_db)):
    owner = _get_logged_user(request)
    post = post_service.get_post_by_id(db, post_id)
    if not post or post.owner != owner or not owner:
        return HTMLResponse("", status_code=403)
    result = post_service.delete_post(db, post_id)
    if result.get("thread_deleted"):
        board_id = result.get("board_id")
        redirect_url = f"/boards/{board_id}" if board_id else "/"
        return HTMLResponse(
            "",
            status_code=200,
            headers={"HX-Redirect": redirect_url},
        )
    return HTMLResponse("")


@router.put("/pages/posts/{post_id}", include_in_schema=False)
def edit_post_htmx(
    post_id: int, request: Request, content: str = Form(...), db: Session = Depends(get_db)
):
    owner = _get_logged_user(request)
    post = post_service.get_post_by_id(db, post_id)
    if not post or post.owner != owner or not owner:
        return HTMLResponse("", status_code=403)
    updated = post_service.update_post_content(db, post_id, content)
    return templates.TemplateResponse(
        "components/post.html", {"request": request, "post": updated, "logged_user": owner}
    )


@router.get("/pages/posts/{post_id}/edits", include_in_schema=False)
def get_post_edits_htmx(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = post_service.get_post_by_id(db, post_id)
    if not post:
        return HTMLResponse("", status_code=404)
    edits = post_service.get_post_edits(db, post_id)
    return templates.TemplateResponse(
        "components/edit_history.html",
        {"request": request, "post": post, "edits": edits},
    )


@router.get("/pages/boards/{board_id}/threads", include_in_schema=False)
def load_more_threads(
    board_id: int, request: Request, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    threads = thread_service.get_all_threads(db, board_id=board_id, limit=limit, offset=offset)
    total_count = thread_service.get_thread_count(db, board_id=board_id)
    logged_user = _get_logged_user(request)

    response_content = ""
    for thread in threads:
        response_content += templates.get_template("components/thread_preview.html").render(
            request=request, thread=thread, logged_user=logged_user
        )

    if offset + len(threads) < total_count:
        next_offset = offset + len(threads)
        response_content += templates.get_template("components/load_more_threads.html").render(
            request=request, board_id=board_id, next_offset=next_offset, limit=limit
        )

    return HTMLResponse(content=response_content)


@router.get("/pages/threads/{thread_id}/posts", include_in_schema=False)
def load_more_posts(
    thread_id: int,
    request: Request,
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    posts = post_service.get_all_posts(db, thread_id=thread_id, limit=limit, offset=offset)
    total_count = post_service.get_post_count(db, thread_id=thread_id)
    logged_user = _get_logged_user(request)

    response_content = ""
    for post in posts:
        response_content += templates.get_template("components/post.html").render(
            request=request, post=post, logged_user=logged_user
        )

    if offset + len(posts) < total_count:
        next_offset = offset + len(posts)
        response_content += templates.get_template("components/load_more_posts.html").render(
            request=request, thread_id=thread_id, next_offset=next_offset, limit=limit
        )

    return HTMLResponse(content=response_content)
