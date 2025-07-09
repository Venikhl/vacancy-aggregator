"""Entry point for vacancy-aggregator-backend application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from .api.v1.router import router as v1_router
from .tasks.parsing import parse_and_store_rabotaru, \
                           parse_and_store_hhru, \
                           parse_and_store_superjob
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
        filename="vacancy-aggregator-backend.log",
        level=logging.INFO
    )
    scheduler.add_job(
        parse_and_store_rabotaru,
        IntervalTrigger(days=1),
        id="rabotaru"
    )
    scheduler.add_job(
        parse_and_store_hhru,
        IntervalTrigger(days=1),
        id="hhru"
    )
    scheduler.add_job(
        parse_and_store_superjob,
        IntervalTrigger(days=1),
        id="superjob"
    )

    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")
