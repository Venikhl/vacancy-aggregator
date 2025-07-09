"""Tasks for parsing and loading into database."""

import logging
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_async_session
from app.database.crud import vacancy as crud_vacancy
from app.services.datasources.rabotaru.scraper import collect_vacancies
from app.services.datasources.HHru import HHAPIParser, VacancyFilters
from app.api.v1.models import Vacancy
from app.core.config import get_settings

logger = logging.getLogger(__name__)

async def store_vacancy(session: AsyncSession, vacancy: Vacancy):
    pass


async def parse_and_store_rabotaru():
    return  # TODO: implement the task

    get_session = get_async_session()
    session = await anext(get_session)
    try:
        logger.info("Scheduled parsing (rabotaru) started")

        vacancies = await collect_vacancies(limit=1024, concurrency=4)
        for vacancy in vacancies:
            await store_vacancy(session, vacancy)

        logger.info("Scheduled parsing (rabotaru) finished")

    except Exception as e:
        logger.error(f"Scheduled task (rabotaru) failed: {e}")
    finally:
        await get_session.aclose()


async def parse_and_store_hhru():
    return  # TODO: implement the task

    get_session = get_async_session()
    session = await anext(get_session)
    settings = get_settings()
    try:
        logger.info("Scheduled parsing (hhru) started")

        parser = HHAPIParser(settings.HH_CLIENT_ID, settings.HH_CLIENT_SECRET)
        filters = VacancyFilters(
            date_from=datetime.now() - timedelta(days=7),
            date_to=datetime.now(),
        )
        async for vacancy in parser.search_all_vacancies(filters):
            vac = Vacancy.model_validate(vacancy.to_dict())
            await store_vacancy(session, vac)

        logger.info("Scheduled parsing (hhru) finished")

    except Exception as e:
        logger.error(f"Scheduled task (hhru) failed: {e}")
    finally:
        await get_session.aclose()


async def parse_and_store_superjob():
    return  # TODO: implement the task

    get_session = get_async_session()
    session = await anext(get_session)
    try:
        logger.info("Scheduled parsing (superjob) started")

        logger.info("Scheduled parsing (superjob) finished")

    except Exception as e:
        logger.error(f"Scheduled task (superjob) failed: {e}")
    finally:
        await get_session.aclose()
