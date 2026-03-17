from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from app.templates import templates

router = APIRouter(tags=["pages"])


@router.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Message Board", "server_time": datetime.now()},
    )


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")
