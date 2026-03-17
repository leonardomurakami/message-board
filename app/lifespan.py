from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """pre-start tasks"""
    Base.metadata.create_all(bind=engine)
    yield
