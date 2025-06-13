"""API models."""

from typing import List
from pydantic import BaseModel


class Register(BaseModel):
    """Registration info."""

    first_name: str
    last_name: str
    email: str
    password: str


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
    current_password: str | None = None
    new_password: str | None = None


class View(BaseModel):
    """Offset and count."""

    offset: int
    count: int


class VacancyFilter(BaseModel):
    """Vacancy filter."""

    pass


class VacanciesView(BaseModel):
    """Vacancy filter, offset, and count."""

    filter: VacancyFilter
    view: View


class ResumeFilter(BaseModel):
    """Resume filter."""

    pass


class ResumesView(BaseModel):
    """Resume filter, offset, and count."""

    filter: ResumeFilter
    view: View


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


class Salary(BaseModel):
    """Salary."""

    type: str
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

    name: str


class ExperienceCategory(BaseModel):
    """Experience category."""

    name: str


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

    time_stamp: str


class Vacancy(BaseModel):
    """Complete representation of vacancy."""

    id: int
    external_id: str
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
    education: str | None = None
    specialization: Specialization | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    published_at: TimeStamp | None = None
