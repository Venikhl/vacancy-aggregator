"""API models."""

from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum


class UserGender(str, Enum):
    """User gender."""

    male = "male"
    female = "female"
    other = "other"


class Register(BaseModel):
    """Registration info."""

    first_name: str
    last_name: str
    email: str
    password: str
    gender: UserGender
    birth_date: date


class Login(BaseModel):
    """Login info."""

    email: str
    password: str


class RefreshToken(BaseModel):
    """Refresh token."""

    refresh_token: str


class UpdateMe(BaseModel):
    """New user information. `None` means leave unchanged."""

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    gender: UserGender | None = None
    birth_date: date | None = None
    current_password: str | None = None
    new_password: str | None = None


class View(BaseModel):
    """Offset and count."""

    offset: int
    count: int


class Tokens(BaseModel):
    """Access and refresh token pair."""

    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    """Access token."""

    access_token: str


class User(BaseModel):
    """User info."""

    first_name: str
    last_name: str
    email: str
    birth_date: date | None
    gender: UserGender | None
    profile_pic_url: str | None

class Education(BaseModel): 
    university : str | None
    faculty: str | None 
    speciality: str | None 
    

class Salary(BaseModel):
    """Salary."""

    type: str | None = None
    currency: str | None = None
    value: int | None = None
    """
    Fixed point number.
    1 means 0.01, 11 means 0.11, 111 means 1.11, etc.
    """


class VacancyShort(BaseModel):
    """Short representation of vacancy."""

    id: int
    title: str
    description: str | None = None
    salary: Salary


class VacancyList(BaseModel):
    """List of vacancies."""

    count: int
    """The total number of results."""
    vacancies: List[VacancyShort]


class ResumeShort(BaseModel):
    """Short representation of resume."""

    id: int
    title: str
    salary: Salary
    description: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None


class ResumeList(BaseModel):
    """List of resumes."""

    count: int
    """The total number of results."""
    resumes: List[ResumeShort]


class Source(BaseModel):
    """Source."""

    name: str


class Company(BaseModel):
    """Company."""

    name: str | None


class ExperienceCategory(BaseModel):
    """Experience category."""

    name: str
    years_of_experience: int| str | None = None


class Location(BaseModel):
    """Location."""

    region: str


class Specialization(BaseModel):
    """Specialization."""

    specialization: str


class EmploymentType(BaseModel):
    """Employment type."""

    name: str


class TimeStamp(BaseModel):
    """Timestamp."""

    time_stamp: str | int


class VacancyFilter(BaseModel):
    """Vacancy filter."""

    title: str | None
    salary_min: int | None
    salary_max: int | None
    experience_categories: List[ExperienceCategory]
    location: Location | None
    date_published_from: Optional[int] | None
    date_published_to: Optional[int] | None


class VacanciesView(BaseModel):
    """Vacancy filter, offset, and count."""

    filter: VacancyFilter
    view: View


class Vacancy(BaseModel):
    """Complete representation of vacancy."""

    id: int
    external_id: str | int
    source: Source | None = None
    title: str
    description: str | None = None
    company: Company | None = None
    salary: Salary
    experience_category: ExperienceCategory | None = None
    location: Location | None = None
    specialization: Specialization | None = None
    employment_types: List[EmploymentType]
    published_at: TimeStamp | None = None
    contacts: str | None = None
    url: str | None = None


class ResumeFilter(BaseModel):
    """Resume filter."""

    title: str | None
    location: Location | None
    salary_min: int | None
    salary_max: int | None
    experience_categories: List[ExperienceCategory]
    skills: List[str]


class ResumesView(BaseModel):
    """Resume filter, offset, and count."""

    filter: ResumeFilter
    view: View


class Resume(BaseModel):
    """Complete representation of resume."""

    id: int
    external_id: str
    source: Source | None = None
    title: str
    salary: Salary
    description: str | None = None
    location: Location | None = None
    experience_category: ExperienceCategory | None = None
    employment: str | None = None
    skills: str | None = None
    education: str | None = None
    specialization: Specialization | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    published_at: TimeStamp | None = None


class ErrorResponse(BaseModel):
    """Error response."""

    detail: str
    code: Optional[int] = None
    error_type: Optional[str] = None
