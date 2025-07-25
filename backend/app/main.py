"""Entry point for vacancy-aggregator-backend application."""

from sys import stdout
from app.core.config import get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from .api.v1.router import router as v1_router
from .tasks.parsing import parse_services
import logging

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Define the application lifespan.

    Everything before `yield` statement gets
    executed on startup. Everything after -
    on shutdown.
    """
    logging.basicConfig(
        stream=stdout,
        level=logging.INFO
    )
    scheduler.add_job(
        parse_services,
        IntervalTrigger(days=1),
        id="parsing"
    )

    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
settings = get_settings()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    f"{settings.PROTOCOL}://{settings.HOST}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")
