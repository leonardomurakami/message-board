import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.lifespan import lifespan
from app.routers import boards, pages, posts, threads


def create_app() -> FastAPI:
    app = FastAPI(title="Message Board", lifespan=lifespan)

    app.include_router(boards.router, prefix="/api")
    app.include_router(threads.router, prefix="/api")
    app.include_router(posts.router, prefix="/api")
    app.include_router(pages.router)

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    return app


app = create_app()


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)


if __name__ == "__main__":
    start()
