import os
import aiohttp
import asyncio
import logging
import time
import backoff
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
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
    """Complete vacancy record structure."""
    vacancy_id: Optional[int]
    external_id: str
    source_id: int
    title: str
    description: Optional[str]
    company_id: Optional[int]
    salary_type_id: Optional[int]
    salary_currency: Optional[str]
    salary_value: Optional[float]
    experience_category_id: Optional[int]
    location_id: Optional[int]
    specialization_id: Optional[int]
    published_at: Optional[str]
    contacts: Optional[str]
    url: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'vacancy_id': self.vacancy_id,
            'external_id': self.external_id,
            'source_id': self.source_id,
            'title': self.title,
            'description': self.description,
            'company_id': self.company_id,
            'salary_type_id': self.salary_type_id,
            'salary_currency': self.salary_currency,
            'salary_value': self.salary_value,
            'experience_category_id': self.experience_category_id,
            'location_id': self.location_id,
            'specialization_id': self.specialization_id,
            'published_at': self.published_at,
            'contacts': self.contacts,
            'url': self.url
        }


@dataclass
class RateLimiter:
    """Basic rate limiter for API requests."""
    max_requests_per_second: float = 2.0
    _requests: List[float] = field(default_factory=list)

    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        now = time.time()

        # Clean old requests
        self._requests = [req_time for req_time in self._requests if now - req_time < 1.0]

        # Check if we need to wait
        if len(self._requests) >= self.max_requests_per_second:
            sleep_time = 1.0 - (now - self._requests[0]) + 0.1
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                return await self.acquire()

        self._requests.append(now)


class HHAPIError(Exception):
    """Base exception for HH API errors."""
    pass


class HHRateLimitError(HHAPIError):
    """Exception raised when rate limit is exceeded."""
    pass


class HHAuthenticationError(HHAPIError):
    """Exception raised for authentication errors."""
    pass


class HHAPIParser:
    """Basic HH.ru API Parser."""

    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        """Initialize HH API Parser with environment variables."""
        self.rate_limiter = RateLimiter()
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

    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, HHRateLimitError),
        max_tries=5,
        factor=2,
        max_time=300
    )
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request with retry logic."""
        await self.rate_limiter.acquire()

        if not self.session:
            raise HHAPIError("Session not initialized")

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = {}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        try:
            async with self.session.request(method, url, params=params, headers=headers) as response:
                if response.status == 429:
                    self.logger.warning("Rate limit exceeded (429)")
                    raise HHRateLimitError("Rate limit exceeded")

                if response.status == 401:
                    raise HHAuthenticationError("Authentication failed")

                if response.status >= 400:
                    raise HHAPIError(f"API request failed: {response.status}")

                return await response.json()

        except asyncio.TimeoutError:
            self.logger.error("Request timeout")
            raise
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error: {e}")
            raise

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

    def _extract_salary_info(self, salary_data: Optional[Dict]) -> tuple:
        """Extract salary information and determine salary type."""
        if not salary_data:
            return None, None, None

        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency')

        if salary_from and salary_to:
            salary_type_id = 3  # Range
            salary_value = (salary_from + salary_to) / 2
        elif salary_from:
            salary_type_id = 1  # From
            salary_value = salary_from
        elif salary_to:
            salary_type_id = 2  # Up to
            salary_value = salary_to
        else:
            salary_type_id = None
            salary_value = None

        return salary_type_id, currency, salary_value

    async def get_vacancy_details(self, vacancy_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific vacancy."""
        return await self._make_request('GET', f'/vacancies/{vacancy_id}')

    def _map_experience_to_category(self, experience_data: Optional[Dict]) -> Optional[int]:
        """Map HH experience to category ID."""
        if not experience_data:
            return None

        exp_id = experience_data.get('id', '')
        mapping = {
            'noExperience': 1,
            'between1And3': 2,
            'between3And6': 3,
            'moreThan6': 4
        }
        return mapping.get(exp_id)

    async def _convert_to_vacancy_record(self, vacancy_data: Dict, source_id: int = 1) -> VacancyRecord:
        """Convert HH API vacancy data to structured VacancyRecord."""
        salary_type_id, salary_currency, salary_value = self._extract_salary_info(
            vacancy_data.get('salary')
        )

        return VacancyRecord(
            vacancy_id=None,
            external_id=str(vacancy_data['id']),
            source_id=source_id,
            title=vacancy_data.get('name', ''),
            description=vacancy_data.get('snippet', {}).get('requirement', ''),
            company_id=None,
            salary_type_id=salary_type_id,
            salary_currency=salary_currency,
            salary_value=salary_value,
            experience_category_id=self._map_experience_to_category(vacancy_data.get('experience')),
            location_id=None,
            specialization_id=vacancy_data.get('professional_roles', [{}])[0].get('id') if vacancy_data.get(
                'professional_roles') else None,
            published_at=vacancy_data.get('published_at'),
            contacts=None,
            url=vacancy_data.get('alternate_url')
        )