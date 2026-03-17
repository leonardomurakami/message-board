from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.models.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Message Board", lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "Health check for now"}


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
