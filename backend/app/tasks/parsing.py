"""Tasks for parsing and loading into database."""

import logging
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.database import get_async_session
from app.database.crud import vacancy as crud_vacancy, \
    source as crud_source, company as crud_company, \
    salary_type as crud_salary_type, \
    experience_category as crud_experience_category, \
    location as crud_location, specialization as crud_specialization, \
    employment_type as crud_employment_type
from app.database.models import Source as DBSource, \
    Company as DBCompany, SalaryType as DBSalaryType, \
    ExperienceCategory as DBExperienceCategory, \
    Location as DBLocation, Specialization as DBSpecialization, \
    EmploymentType as DBEmploymentType, Vacancy as DBVacancy
from app.services.datasources.base import VacancyParser
from app.services.datasources.SuperJob import SuperJobParser
from app.services.datasources.HHru import HHVacancyParser
from app.api.v1.models import ExperienceCategory, Location, Vacancy, \
    Source, Company, Specialization, EmploymentType, VacancyFilter

logger = logging.getLogger(__name__)


async def store_source(
    session: AsyncSession,
    source: Source
) -> DBSource:
    """Store source in database if not exists."""
    result = await session.execute(
        select(DBSource).where(DBSource.name == source.name)
    )
    found = result.scalars().first()
    if not found:
        created = await crud_source.create(
            session,
            obj_in={"name": source.name}
        )
        return created
    return found


async def store_company(
    session: AsyncSession,
    company: Company
) -> DBCompany:
    """Store company in database if not exists."""
    result = await session.execute(
        select(DBCompany).where(DBCompany.name == company.name)
    )
    found = result.scalars().first()
    if not found:
        created = await crud_company.create(
            session,
            obj_in={"name": company.name}
        )
        return created
    return found


async def store_salary_type(
    session: AsyncSession,
    salary_type: str
) -> DBSalaryType:
    """Store salary type in database if not exists."""
    result = await session.execute(
        select(DBSalaryType).where(DBSalaryType.name == salary_type)
    )
    found = result.scalars().first()
    if not found:
        created = await crud_salary_type.create(
            session,
            obj_in={"name": salary_type}
        )
        return created
    return found


async def store_experience_category(
    session: AsyncSession,
    experience_category: ExperienceCategory
) -> DBExperienceCategory:
    """Store experience category in database if not exists."""
    result = await session.execute(
        select(DBExperienceCategory).where(
            DBExperienceCategory.name == experience_category.name
        )
    )
    found = result.scalars().first()
    if not found:
        created = await crud_experience_category.create(
            session,
            obj_in={"name": experience_category.name}
        )
        return created
    return found


async def store_location(
    session: AsyncSession,
    location: Location
) -> DBLocation:
    """Store location in database if not exists."""
    result = await session.execute(
        select(DBLocation).where(DBLocation.region == location.region)
    )
    found = result.scalars().first()
    if not found:
        created = await crud_location.create(
            session,
            obj_in={"region": location.region}
        )
        return created
    return found


async def store_specialization(
    session: AsyncSession,
    specialization: Specialization
) -> DBSpecialization:
    """Store specialization in database if not exists."""
    result = await session.execute(
        select(DBSpecialization).where(
            DBSpecialization.specialization == specialization.specialization
        )
    )
    found = result.scalars().first()
    if not found:
        created = await crud_specialization.create(
            session,
            obj_in={"specialization": specialization.specialization}
        )
        return created
    return found


async def store_employment_type(
    session: AsyncSession,
    employment_type: EmploymentType
) -> DBEmploymentType:
    """Store employment type in database if not exists."""
    result = await session.execute(
        select(DBEmploymentType).where(
            DBEmploymentType.name == employment_type.name
        )
    )
    found = result.scalars().first()
    if not found:
        created = await crud_employment_type.create(
            session,
            obj_in={"name": employment_type.name}
        )
        return created
    return found


async def store_vacancy(
    session: AsyncSession,
    vacancy: Vacancy
) -> DBVacancy:
    """Store vacancy in database."""
    db_source = None
    db_company = None
    db_salary_type = None
    db_experience_category = None
    db_location = None
    db_specialization = None
    db_employment_types = []
    if vacancy.source:
        db_source = await store_source(session, vacancy.source)
    if vacancy.company:
        db_company = await store_company(session, vacancy.company)
    if vacancy.salary.type:
        db_salary_type = await store_salary_type(
            session, vacancy.salary.type
        )
    if vacancy.experience_category:
        db_experience_category = await store_experience_category(
            session, vacancy.experience_category
        )
    if vacancy.location:
        db_location = await store_location(
            session, vacancy.location
        )
    if vacancy.specialization:
        db_specialization = await store_specialization(
            session, vacancy.specialization
        )
    for employment_type in vacancy.employment_types:
        db_employment_types.append(
            await store_employment_type(session, employment_type)
        )

    source_id = None
    company_id = None
    salary_type_id = None
    location_id = None
    experience_category_id = None
    specialization_id = None
    published_at = None
    if db_source:
        source_id = db_source.id
    if db_company:
        company_id = db_company.id
    if db_salary_type:
        salary_type_id = db_salary_type.id
    if db_location:
        location_id = db_location.id
    if db_experience_category:
        experience_category_id = db_experience_category.id
    if db_specialization:
        specialization_id = db_specialization.id
    if vacancy.published_at:
        date_string = vacancy.published_at.time_stamp
        published_at = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

    created = await crud_vacancy.create(
        session,
        obj_in={
            "external_id": vacancy.external_id,
            "source_id": source_id,
            "title": vacancy.title,
            "description": vacancy.description,
            "company_id": company_id,
            "salary_type_id": salary_type_id,
            "salary_currency": vacancy.salary.currency,
            "salary_value": vacancy.salary.value,
            "experience_category_id": experience_category_id,
            "location_id": location_id,
            "specialization_id": specialization_id,
            "published_at": published_at,
            "contacts": vacancy.contacts,
            "url": vacancy.url
        }
    )

    for db_employment_type in db_employment_types:
        created.employment_types.append(db_employment_type)
        await session.commit()
        await session.refresh(created)

    return created


async def parse_services():
    """Parse and store vacancies from all services."""
    try:
        session_gen = get_async_session()
        session = await session_gen.__anext__()

        parsers: List[VacancyParser] = [
            SuperJobParser(),
            HHVacancyParser(),
        ]
        date_from = datetime.now() - timedelta(days=1)
        date_to = datetime.now()
        filter = VacancyFilter(
            title=None,
            salary_min=None,
            salary_max=None,
            experience_categories=[],
            location=None,
            date_published_from=int(date_from.timestamp()),
            date_published_to=int(date_to.timestamp())
        )
        for parser in parsers:
            logger.info(f"Running parser `{parser.parser_name}`")
            async with parser:
                async for vacancy in parser.search_vacancies(filter, 200):
                    logger.info(f"Storing vacancy {vacancy}")
                    try:
                        await store_vacancy(session, vacancy)
                    except Exception as e:
                        logger.error(f"Failed to store vacancy: {e}")
    except Exception as e:
        logger.info(f"Something went wrong while parsing: {e}")


async def cleanup():
    pass
