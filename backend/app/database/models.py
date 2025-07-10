"""Database models for the vacancy aggregator application.

This module contains all SQLAlchemy ORM models representing database tables
and their relationships for the vacancy aggregator system.
"""

from sqlalchemy import (
    Column, Integer, String, Text,
    Numeric, TIMESTAMP, ForeignKey, Table
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.types import Date, Enum
from app.api.v1.models import UserGender


class Base(DeclarativeBase):
    """Base model."""

    pass


# Association tables for many-to-many relationships
vacancy_employment_type = Table(
    'Vacancy_EmploymentType',
    Base.metadata,
    Column('vacancy_id', Integer,
           ForeignKey('Vacancy.id'), primary_key=True),
    Column('employment_type_id', Integer,
           ForeignKey('EmploymentType.id'),
           primary_key=True)
)

user_favorite_vacancies = Table(
    'User_Favorite_Vacancies',
    Base.metadata,
    Column('user_id', Integer,
           ForeignKey('User.id'), primary_key=True),
    Column('vacancy_id', Integer,
           ForeignKey('Vacancy.id'), primary_key=True)
)

user_favorite_resumes = Table(
    'User_Favorite_Resumes',
    Base.metadata,
    Column('user_id', Integer,
           ForeignKey('User.id'), primary_key=True),
    Column('resume_id', Integer,
           ForeignKey('Resume.id'), primary_key=True)
)


class User(Base):
    """User model representing registered users of the system."""

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(200))
    birth_date = Column(Date)
    gender = Column(Enum(UserGender, name="user_gender"))
    hashed_password = Column(String(100))


    favorite_vacancies = relationship(
        "Vacancy",
        secondary=user_favorite_vacancies,
        backref="users_who_favorited"
    )
    favorite_resumes = relationship(
        "Resume",
        secondary=user_favorite_resumes,
        backref="users_who_favorited"
    )


class Vacancy(Base):
    """Job vacancy model containing all job posting information."""

    __tablename__ = 'Vacancy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(100), nullable=False)
    source_id = Column(Integer, ForeignKey('Source.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey('Company.id'))
    salary_type_id = Column(Integer, ForeignKey('SalaryType.id'))
    salary_currency = Column(String(50))
    salary_value = Column(Numeric(10, 2))
    experience_category_id = Column(
        Integer, ForeignKey('ExperienceCategory.id'))
    location_id = Column(Integer, ForeignKey('Location.id'))
    specialization_id = Column(
        Integer, ForeignKey('Specialization.id'))
    published_at = Column(TIMESTAMP(timezone=True))
    contacts = Column(Text)
    url = Column(String(255))

    employment_types = relationship(
        "EmploymentType",
        secondary=vacancy_employment_type,
        backref="vacancies"
    )
    company = relationship("Company", backref="vacancies")
    source = relationship("Source", backref="vacancies")
    salary_type = relationship("SalaryType", backref="vacancies")
    experience_category = relationship("ExperienceCategory",
                                       backref="vacancies")
    location = relationship("Location", backref="vacancies")
    specialization = relationship("Specialization", backref="vacancies")


class Location(Base):
    """Geographical location model for vacancies and resumes."""

    __tablename__ = 'Location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String(100))


class Specialization(Base):
    """Professional specialization or job category model."""

    __tablename__ = 'Specialization'

    id = Column(Integer, primary_key=True, autoincrement=True)
    specialization = Column(String(255))


class EmploymentType(Base):
    """Type of employment (full-time, part-time, etc.)."""

    __tablename__ = 'EmploymentType'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))


class Company(Base):
    """Company model representing employers posting vacancies."""

    __tablename__ = 'Company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class ExperienceCategory(Base):
    """Experience level classification for jobs and candidates."""

    __tablename__ = 'ExperienceCategory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class Source(Base):
    """Source of vacancies or resumes (job board, API, etc.)."""

    __tablename__ = 'Source'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class SalaryType(Base):
    """Type of salary (gross, net, hourly, etc.)."""

    __tablename__ = 'SalaryType'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class Resume(Base):
    """Candidate resume model containing professional information."""

    __tablename__ = 'Resume'

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(100), nullable=False)
    source_id = Column(Integer, ForeignKey('Source.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    salary_type_id = Column(Integer, ForeignKey('SalaryType.id'))
    salary_currency = Column(String(50))
    salary_value = Column(Numeric(10, 2))
    skills_text = Column(Text)
    location_id = Column(Integer, ForeignKey('Location.id'))
    experience_category_id = Column(
        Integer, ForeignKey('ExperienceCategory.id'))
    education = Column(Text)
    specialization_id = Column(
        Integer, ForeignKey('Specialization.id'))
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100))
    email = Column(String(255))
    phone_number = Column(String(50))
    published_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    source = relationship("Source", backref="resumes")
    salary_type = relationship("SalaryType", backref="resumes")
    location = relationship("Location", backref="resumes")
    experience_category = relationship("ExperienceCategory", backref="resumes")
    specialization = relationship("Specialization", backref="resumes")
