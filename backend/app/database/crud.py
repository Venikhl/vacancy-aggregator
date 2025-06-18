"""CRUD operations."""

from typing import List, Optional, Tuple, Type, TypeVar
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from datetime import datetime
from pydantic import BaseModel
from .models import (
    User, Vacancy, Resume, Company, Location,
    Specialization, EmploymentType, ExperienceCategory,
    Source, SalaryType, vacancy_employment_type,
    user_favorite_vacancies, user_favorite_resumes
)


ModelType = TypeVar('ModelType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase:
    """
    Base class for CRUD operations on SQLAlchemy models.

    Attributes:
        model (Type[ModelType]): The SQLAlchemy model class to operate on.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUDBase with the given model.

        Args:
            model (Type[ModelType]): SQLAlchemy model class.
        """
        self.model = model

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        """
        Create a new instance in the database.

        Args:
            db (AsyncSession): Async database session.
            obj_in (dict): Data to create the object.

        Returns:
            ModelType: The newly created object.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Retrieve a single object by ID.

        Args:
            db (AsyncSession): Async database session.
            id (int): Object ID.

        Returns:
            Optional[ModelType]: The object if found, otherwise None.
        """
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve multiple objects with pagination.

        Args:
            db (AsyncSession): Async database session.
            skip (int): Number of records to skip.
            limit (int): Maximum number of records to retrieve.

        Returns:
            List[ModelType]: List of retrieved objects.
        """
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: dict
    ) -> ModelType:
        """
        Update an existing object.

        Args:
            db (AsyncSession): Async database session.
            db_obj (ModelType): Existing object from the database.
            obj_in (dict): Fields to update.

        Returns:
            ModelType: The updated object.
        """
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        """
        Delete an object by ID.

        Args:
            db (AsyncSession): Async database session.
            id (int): ID of the object to delete.

        Returns:
            ModelType: The deleted object.
        """
        obj = await self.get(db, id=id)
        await db.delete(obj)
        await db.commit()
        return obj


class CRUDVacancy(CRUDBase):
    """CRUD operations specifically for Vacancy model."""

    def __init__(self):
        """Initialize CRUDVacancy."""
        super().__init__(Vacancy)

    async def get_with_relations(
        self,
        db: AsyncSession,
        vacancy_id: int
    ) -> Optional[Vacancy]:
        """
        Get a vacancy along with its related data.

        Args:
            db (AsyncSession): Async database session.
            vacancy_id (int): ID of the vacancy.

        Returns:
            Optional[Vacancy]: Vacancy object with related fields loaded.
        """
        result = await db.execute(
            select(Vacancy)
            .options(
                joinedload(Vacancy.company),
                joinedload(Vacancy.source),
                joinedload(Vacancy.location),
                joinedload(Vacancy.specialization),
                joinedload(Vacancy.experience_category),
                joinedload(Vacancy.employment_types),
                joinedload(Vacancy.salary_type)
            )
            .where(Vacancy.vacancy_id == vacancy_id)
        )
        return result.scalars().first()

    async def search(
        self,
        db: AsyncSession,
        *,
        title: Optional[str] = None,
        company_id: Optional[int] = None,
        specialization_id: Optional[int] = None,
        min_salary: Optional[float] = None,
        max_salary: Optional[float] = None,
        experience_category_ids: Optional[List[int]] = None,
        location_id: Optional[int] = None,
        employment_type_ids: Optional[List[int]] = None,
        published_after: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Vacancy]:
        """
        Search for vacancies with various filters.

        Args:
            db (AsyncSession): Async database session.
            title (str, optional): Vacancy title to search.
            company_id (int, optional): Company filter.
            specialization_id (int, optional): Specialization filter.
            min_salary (float, optional): Minimum salary.
            max_salary (float, optional): Maximum salary.
            experience_category_id (int, optional): Experience filter.
            location_id (int, optional): Location filter.
            employment_type_ids (List[int], optional): Employment types.
            published_after (datetime, optional): Filter by published date.
            skip (int): Pagination offset.
            limit (int): Pagination limit.

        Returns:
            List[Vacancy]: List of matching vacancies.
        """
        query = select(Vacancy).options(
            joinedload(Vacancy.company),
            joinedload(Vacancy.location)
        )

        filters = []
        if title:
            filters.append(Vacancy.title.ilike(f"%{title}%"))
        if company_id:
            filters.append(Vacancy.company_id == company_id)
        if specialization_id:
            filters.append(Vacancy.specialization_id == specialization_id)
        if min_salary:
            filters.append(Vacancy.salary_value >= min_salary)
        if max_salary:
            filters.append(Vacancy.salary_value <= max_salary)
        if experience_category_ids:
            experience_category_filters = [
                Vacancy.experience_category_id == id
                for id in experience_category_ids
            ]
            filters.append(or_(*experience_category_filters))
        if location_id:
            filters.append(Vacancy.location_id == location_id)
        if published_after:
            filters.append(Vacancy.published_at >= published_after)
        if employment_type_ids:
            query = query.join(
                vacancy_employment_type,
                Vacancy.vacancy_id == vacancy_employment_type.c.vacancy_id
            )
            filters.append(
                vacancy_employment_type.c.employment_type_id.in_(
                    employment_type_ids)
            )

        if filters:
            query = query.where(and_(*filters))

        result = await db.execute(
            query
            .offset(skip)
            .limit(limit)
            .distinct()
        )
        return result.scalars().all()


class CRUDResume(CRUDBase):
    """CRUD operations for Resume model."""

    def __init__(self):
        """Initialize CRUDResume."""
        super().__init__(Resume)

    async def get_with_relations(
        self,
        db: AsyncSession,
        resume_id: int
    ) -> Optional[Resume]:
        """
        Get a resume along with its related data.

        Args:
            db (AsyncSession): Async database session.
            resume_id (int): ID of the resume.

        Returns:
            Optional[Resume]: Resume object with related fields loaded.
        """
        result = await db.execute(
            select(Resume)
            .options(
                joinedload(Resume.source),
                joinedload(Resume.salary_type),
                joinedload(Resume.location),
                joinedload(Resume.experience_category),
                joinedload(Resume.specialization)
            )
            .where(Resume.resume_id == resume_id)
        )
        return result.scalars().first()

    async def search(
        self,
        db: AsyncSession,
        *,
        title: Optional[str] = None,
        specialization_id: Optional[int] = None,
        min_salary: Optional[float] = None,
        max_salary: Optional[float] = None,
        experience_category_ids: Optional[List[int]] = None,
        location_id: Optional[int] = None,
        skills: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Resume]:
        """
        Search resumes using various filters.

        Args:
            db (AsyncSession): Async database session.
            title (str, optional): Resume title.
            specialization_id (int, optional): Specialization filter.
            min_salary (float, optional): Minimum expected salary.
            max_salary (float, optional): Maximum expected salary.
            experience_category_id (int, optional): Experience level.
            location_id (int, optional): Location filter.
            skills (List[str], optional): Required skills (partial match).
            skip (int): Pagination offset.
            limit (int): Pagination limit.

        Returns:
            List[Resume]: Filtered list of resumes.
        """
        query = select(Resume).options(
            joinedload(Resume.location),
            joinedload(Resume.specialization)
        )

        filters = []
        if title:
            filters.append(Resume.title.ilike(f"%{title}%"))
        if specialization_id:
            filters.append(Resume.specialization_id == specialization_id)
        if min_salary:
            filters.append(Resume.salary_value >= min_salary)
        if max_salary:
            filters.append(Resume.salary_value <= max_salary)
        if experience_category_ids:
            experience_category_filters = [
                Resume.experience_category_id == id
                for id in experience_category_ids
            ]
            filters.append(or_(*experience_category_filters))
        if location_id:
            filters.append(Resume.location_id == location_id)
        if skills:
            skill_filters = [
                Resume.skills_text.ilike(f"%{skill}%") for skill in skills
            ]
            filters.append(or_(*skill_filters))

        if filters:
            query = query.where(and_(*filters))

        result = await db.execute(
            query
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDUser(CRUDBase):
    """CRUD operations and business logic for User model."""

    def __init__(self):
        """Initialize CRUDVacancy."""
        super().__init__(User)

    async def get_by_email(
            self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by email.

        Args:
            db (AsyncSession): Async database session.
            email (str): User email.

        Returns:
            Optional[User]: User object if found.
        """
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_by_id(
            self, db: AsyncSession, id: int) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            db (AsyncSession): Async database session.
            id (int): User ID.

        Returns:
            Optional[User]: User object if found.
        """
        result = await db.execute(
            select(User).where(User.user_id == id)
        )
        return result.scalars().first()

    async def add_favorite_vacancy(
        self,
        db: AsyncSession,
        user_id: int,
        vacancy_id: int
    ) -> Optional[User]:
        """
        Add a vacancy to user's favorites.

        Args:
            db (AsyncSession): Async database session.
            user_id (int): ID of the user.
            vacancy_id (int): ID of the vacancy.

        Returns:
            Optional[User]: Updated user object.
        """
        user = await self.get(db, id=user_id)
        if user:
            stmt = select(Vacancy).where(Vacancy.vacancy_id == vacancy_id)
            result = await db.execute(stmt)
            vacancy = result.scalars().first()
            if vacancy:
                user.favorite_vacancies.append(vacancy)
                await db.commit()
                await db.refresh(user)
        return user

    async def remove_favorite_vacancy(
        self,
        db: AsyncSession,
        user_id: int,
        vacancy_id: int
    ) -> Optional[User]:
        """
        Remove a vacancy from user's favorites.

        Args:
            db (AsyncSession): Async database session.
            user_id (int): ID of the user.
            vacancy_id (int): ID of the vacancy.

        Returns:
            Optional[User]: Updated user object.
        """
        user = await self.get(db, id=user_id)
        if user:
            stmt = select(Vacancy).where(Vacancy.vacancy_id == vacancy_id)
            result = await db.execute(stmt)
            vacancy = result.scalars().first()
            if vacancy and vacancy in user.favorite_vacancies:
                user.favorite_vacancies.remove(vacancy)
                await db.commit()
                await db.refresh(user)
        return user

    async def get_favorite_vacancies(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[Vacancy]]:
        """
        Retrieve user's favorite vacancies.

        Args:
            db (AsyncSession): Async database session.
            user_id (int): ID of the user.
            skip (int): Offset for pagination.
            limit (int): Max number of results.

        Returns:
            (int, List[Vacancy]): Total count and paginated list
            of favorite vacancies.
        """
        user = await self.get(db, id=user_id)
        if not user:
            return (0, [])

        result = await db.execute(
            select(Vacancy)
            .join(user_favorite_vacancies)
            .where(user_favorite_vacancies.c.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        count_result = await db.execute(
            select(func.count())
            .select_from(user_favorite_vacancies)
            .where(user_favorite_vacancies.c.user_id == user_id)
        )

        return (count_result.scalar_one(), result.scalars().all())

    async def add_favorite_resume(
        self,
        db: AsyncSession,
        user_id: int,
        resume_id: int
    ) -> Optional[User]:
        """
        Add a resume to user's favorites.

        Args:
            db (AsyncSession): Async database session.
            user_id (int): ID of the user.
            resume_id (int): ID of the resume.

        Returns:
            Optional[User]: Updated user object.
        """
        user = await self.get(db, id=user_id)
        if user:
            stmt = select(Resume).where(Resume.resume_id == resume_id)
            result = await db.execute(stmt)
            resume = result.scalars().first()
            if resume:
                user.favorite_resumes.append(resume)
                await db.commit()
                await db.refresh(user)
        return user

    async def remove_favorite_resume(
        self,
        db: AsyncSession,
        user_id: int,
        resume_id: int
    ) -> Optional[User]:
        """
        Remove a resume from user's favorites.

        Args:
            db (AsyncSession): Async database session.
            user_id (int): ID of the user.
            resume_id (int): ID of the resume.

        Returns:
            Optional[User]: Updated user object.
        """
        user = await self.get(db, id=user_id)
        if user:
            stmt = select(Resume).where(Resume.resume_id == resume_id)
            result = await db.execute(stmt)
            resume = result.scalars().first()
            if resume and resume in user.favorite_resumes:
                user.favorite_resumes.remove(resume)
                await db.commit()
                await db.refresh(user)
        return user

    async def get_favorite_resumes(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[int, List[Resume]]:
        """
        Retrieve user's favorite resumes with related data.

        Args:
            db (AsyncSession): Async database session.
            user_id (int): ID of the user.
            skip (int): Pagination offset.
            limit (int): Pagination limit.

        Returns:
            List[Resume]: Total count and paginated list
            of favorite resumes.
        """
        user = await self.get(db, id=user_id)
        if not user:
            return (0, [])

        result = await db.execute(
            select(Resume)
            .options(
                joinedload(Resume.location),
                joinedload(Resume.specialization),
                joinedload(Resume.experience_category)
            )
            .join(user_favorite_resumes)
            .where(user_favorite_resumes.c.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        count_result = await db.execute(
            select(func.count())
            .select_from(user_favorite_resumes)
            .where(user_favorite_resumes.c.user_id == user_id)
        )
        return (count_result.scalar_one(), result.scalars().unique().all())


# CRUD instances
user = CRUDUser()
vacancy = CRUDVacancy()
resume = CRUDResume()
company = CRUDBase(Company)
location = CRUDBase(Location)
specialization = CRUDBase(Specialization)
employment_type = CRUDBase(EmploymentType)
experience_category = CRUDBase(ExperienceCategory)
source = CRUDBase(Source)
salary_type = CRUDBase(SalaryType)
