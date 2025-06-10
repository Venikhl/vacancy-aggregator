import os
import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field, validator


class ExperienceLevel(str, Enum):
    """Experience level enumeration."""
    NO_EXPERIENCE = "noExperience"
    BETWEEN_1_AND_3 = "between1And3"
    BETWEEN_3_AND_6 = "between3And6"
    MORE_THAN_6 = "moreThan6"


class EmploymentType(str, Enum):
    """Employment type enumeration."""
    FULL = "full"
    PART = "part"
    PROJECT = "project"
    VOLUNTEER = "volunteer"
    PROBATION = "probation"


class ScheduleType(str, Enum):
    """Schedule type enumeration."""
    FULL_DAY = "fullDay"
    SHIFT = "shift"
    FLEXIBLE = "flexible"
    REMOTE = "remote"
    FLY_IN_FLY_OUT = "flyInFlyOut"


class VacancyFilters(BaseModel):
    """Vacancy search filters model."""
    text: Optional[str] = Field(None, description="Search text")
    area: Optional[int] = Field(None, description="Area ID")
    professional_role: Optional[int] = Field(None, description="Professional role ID")
    experience: Optional[ExperienceLevel] = Field(None, description="Experience level")
    employment: Optional[EmploymentType] = Field(None, description="Employment type")
    schedule: Optional[ScheduleType] = Field(None, description="Schedule type")


@dataclass
class VacancyRecord:
    """Basic vacancy record structure."""
    vacancy_id: Optional[int]
    external_id: str
    title: str
    url: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'vacancy_id': self.vacancy_id,
            'external_id': self.external_id,
            'title': self.title,
            'url': self.url
        }


class HHAPIError(Exception):
    """Base exception for HH API errors."""
    pass


class HHAuthenticationError(HHAPIError):
    """Exception raised for authentication errors."""
    pass


class HHAPIParser:
    """Basic HH.ru API Parser."""

    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        """Initialize HH API Parser with environment variables."""
        self.client_id = os.getenv('HH_CLIENT_ID')
        self.client_secret = os.getenv('HH_CLIENT_SECRET')
        self.access_token = os.getenv('HH_ACCESS_TOKEN')

        if not all([self.client_id, self.client_secret]):
            raise ValueError("HH_CLIENT_ID and HH_CLIENT_SECRET must be set in environment")

        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to HH API."""
        if not self.session:
            raise HHAPIError("Session not initialized")

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = {}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        async with self.session.request(method, url, params=params, headers=headers) as response:
            if response.status == 401:
                raise HHAuthenticationError("Authentication failed")
            if response.status >= 400:
                raise HHAPIError(f"API request failed: {response.status}")

            return await response.json()

    async def _search_vacancies_page(self, filters: VacancyFilters, page: int = 0) -> Dict[str, Any]:
        """Search vacancies for a specific page."""
        params = {
            'page': page,
            'per_page': 100,
        }

        if filters.text:
            params['text'] = filters.text
        if filters.area:
            params['area'] = filters.area
        if filters.professional_role:
            params['professional_role'] = filters.professional_role
        if filters.experience:
            params['experience'] = filters.experience.value
        if filters.employment:
            params['employment'] = filters.employment.value
        if filters.schedule:
            params['schedule'] = filters.schedule.value

        return await self._make_request('GET', '/vacancies', params=params)

    async def search_vacancies_simple(self, filters: VacancyFilters) -> List[VacancyRecord]:
        """Simple vacancy search with basic pagination."""
        all_vacancies = []
        page = 0

        while True:
            response = await self._search_vacancies_page(filters, page)
            vacancies = response.get('items', [])
            if not vacancies:
                break

            for vacancy in vacancies:
                record = VacancyRecord(
                    vacancy_id=None,
                    external_id=str(vacancy['id']),
                    title=vacancy.get('name', ''),
                    url=vacancy.get('alternate_url')
                )
                all_vacancies.append(record)

            # Check if we've reached the last page
            if page >= response.get('pages', 1) - 1:
                break
            page += 1

        return all_vacancies