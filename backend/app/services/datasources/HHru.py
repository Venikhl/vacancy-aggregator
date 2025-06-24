import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, AsyncGenerator, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
import backoff
from pydantic import BaseModel, Field, validator
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Configuration and Models
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
    area: Optional[int] = Field(None, description="Area ID (e.g., 1 for Moscow)")
    professional_role: Optional[int] = Field(None, description="professional_role ID")
    industry: Optional[int] = Field(None, description="Industry ID")
    experience: Optional[ExperienceLevel] = Field(None, description="Experience level")
    employment: Optional[EmploymentType] = Field(None, description="Employment type")
    schedule: Optional[ScheduleType] = Field(None, description="Schedule type")
    salary_from: Optional[int] = Field(None, ge=0, description="Minimum salary")
    salary_to: Optional[int] = Field(None, ge=0, description="Maximum salary")
    currency: Optional[str] = Field("RUR", description="Currency code")
    only_with_salary: Optional[bool] = Field(False, description="Only vacancies with salary")
    date_from: Optional[datetime] = Field(None, description="Published from date")
    date_to: Optional[datetime] = Field(None, description="Published to date")

    @validator('salary_to')
    def validate_salary_range(cls, v, values):
        """Validate that salary_to >= salary_from."""
        if v is not None and 'salary_from' in values and values['salary_from'] is not None:
            if v < values['salary_from']:
                raise ValueError('salary_to must be greater than or equal to salary_from')
        return v


@dataclass
class VacancyRecord:
    """Structured vacancy record for JSON output."""
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
    """Enhanced rate limiter for API requests with stricter control."""
    max_requests_per_second: float = 2.0  # Conservative limit
    max_requests_per_minute: int = 100  # Additional minute-based limit
    _requests: List[float] = field(default_factory=list)
    _minute_requests: List[float] = field(default_factory=list)
    _last_429_time: Optional[float] = field(default=None)
    _backoff_factor: float = field(default=1.0)

    async def acquire(self) -> None:
        """Acquire permission to make a request with enhanced rate limiting."""
        now = asyncio.get_event_loop().time()

        # Apply additional backoff if we recently hit 429
        if self._last_429_time and (now - self._last_429_time) < 60:
            self._backoff_factor = min(self._backoff_factor * 1.1, 3.0)
        else:
            self._backoff_factor = max(self._backoff_factor * 0.95, 1.0)

        effective_rps = self.max_requests_per_second / self._backoff_factor

        # Clean old requests (1 second window)
        self._requests = [req_time for req_time in self._requests if now - req_time < 1.0]

        # Clean old minute requests (60 second window)
        self._minute_requests = [req_time for req_time in self._minute_requests if now - req_time < 60.0]

        # Check per-second limit
        if len(self._requests) >= effective_rps:
            sleep_time = 1.0 - (now - self._requests[0]) + 0.1  # Add small buffer
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                return await self.acquire()

        # Check per-minute limit
        if len(self._minute_requests) >= self.max_requests_per_minute:
            sleep_time = 60.0 - (now - self._minute_requests[0]) + 1.0  # Add buffer
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                return await self.acquire()

        # Add mandatory delay between requests
        if self._requests:
            time_since_last = now - self._requests[-1]
            min_interval = 1.0 / effective_rps
            if time_since_last < min_interval:
                await asyncio.sleep(min_interval - time_since_last)
                now = asyncio.get_event_loop().time()

        self._requests.append(now)
        self._minute_requests.append(now)

    def record_429_error(self) -> None:
        """Record that we hit a 429 error."""
        self._last_429_time = asyncio.get_event_loop().time()


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
    """
    Enhanced HH.ru API Parser with comprehensive coverage strategy.

    Features:
    - Aggressive date splitting to bypass 2000 results limit
    - Parameter-based splitting (experience, employment, schedule)
    - Duplicate detection and removal
    - Full vacancy details extraction
    - JSON output format
    """

    BASE_URL = "https://api.hh.ru"
    MAX_RESULTS_PER_REQUEST = 100
    MAX_TOTAL_RESULTS = 2000
    MIN_DATE_RANGE_DAYS = 1  # Minimum date range for splitting

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            access_token: Optional[str] = None,
            rate_limiter: Optional[RateLimiter] = None
    ):
        """Initialize HH API Parser."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.rate_limiter = rate_limiter or RateLimiter(max_requests_per_second=8.0)  # Even more conservative
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)
        self.seen_vacancy_ids: Set[str] = set()
        self.request_count = 0
        self.start_time = time.time()
        self.last_stats_log = time.time()

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60, connect=30),  # Increased timeouts
            headers={'Content-Type': 'application/json'},
            connector=aiohttp.TCPConnector(limit=10, limit_per_host=5)  # Limit concurrent connections
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, HHRateLimitError),
        max_tries=7,  # Increased max tries
        factor=2,
        max_time=600,  # Increased max wait time
        jitter=backoff.full_jitter  # Add jitter to prevent thundering herd
    )
    async def _make_request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict] = None,
            data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make authenticated request to HH API with enhanced retry logic."""
        if not self.session:
            raise HHAPIError("Session not initialized. Use async context manager.")

        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = {'User-Agent': 'HH-Parser/1.0'}  # Add User-Agent
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        try:
            async with self.session.request(
                    method, url, params=params, json=data, headers=headers
            ) as response:

                # Enhanced handling of rate limit responses
                if response.status == 429:
                    self.rate_limiter.record_429_error()
                    retry_after = int(response.headers.get('Retry-After', 120))  # Default 2 min
                    self.logger.warning(f"Rate limit exceeded (429). Waiting {retry_after}s")
                    await asyncio.sleep(retry_after)
                    raise HHRateLimitError("Rate limit exceeded")

                # Handle 403 errors (often rate limiting in disguise)
                if response.status == 403:
                    print(response.text)
                    self.rate_limiter.record_429_error()
                    self.logger.warning("Got 403 error, treating as rate limit. Waiting 60s")
                    await asyncio.sleep(60)  # Wait 1 minute for 403
                    raise HHRateLimitError("Access forbidden (treating as rate limit)")

                # Handle 500+ errors with longer backoff
                if response.status >= 500:
                    self.logger.warning(f"Server error {response.status}, will retry")
                    await asyncio.sleep(10)  # Wait before retry
                    raise HHAPIError(f"Server error: {response.status}")

                if response.status == 401:
                    raise HHAuthenticationError("Authentication failed")

                if response.status >= 400:
                    error_data = await response.json() if response.content_type == 'application/json' else {}
                    error_msg = error_data.get('description', f'HTTP {response.status}')
                    raise HHAPIError(f"API request failed: {error_msg}")

                return await response.json()

        except asyncio.TimeoutError:
            self.logger.error("Request timeout")
            await asyncio.sleep(10)  # Wait before retry on timeout
            raise
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error during API request: {e}")
            # Add delay before retry for network errors
            await asyncio.sleep(5)
            raise
        finally:
            # Track request statistics
            self.request_count += 1
            current_time = time.time()

            # Log stats every 100 requests
            if self.request_count % 100 == 0 or (current_time - self.last_stats_log) > 300:
                elapsed = current_time - self.start_time
                rate = self.request_count / elapsed if elapsed > 0 else 0
                self.logger.info(f"Request stats: {self.request_count} requests, {rate:.2f} req/s average")
                self.last_stats_log = current_time

    def _create_filter_combinations(self, base_filters: VacancyFilters) -> List[VacancyFilters]:
        """Create all possible filter combinations for comprehensive coverage."""
        combinations = []

        # Base combination
        combinations.append(base_filters)

        # Experience level combinations
        for exp_level in ExperienceLevel:
            exp_filters = base_filters.copy()
            exp_filters.experience = exp_level
            combinations.append(exp_filters)

        # Employment type combinations
        for emp_type in EmploymentType:
            emp_filters = base_filters.copy()
            emp_filters.employment = emp_type
            combinations.append(emp_filters)

            # Combined experience + employment
            for exp_level in ExperienceLevel:
                combined_filters = base_filters.copy()
                combined_filters.experience = exp_level
                combined_filters.employment = emp_type
                combinations.append(combined_filters)

        # Schedule type combinations
        for schedule in ScheduleType:
            schedule_filters = base_filters.copy()
            schedule_filters.schedule = schedule
            combinations.append(schedule_filters)

        return combinations

    def _split_date_range_aggressive(
            self,
            date_from: datetime,
            date_to: datetime,
            initial_days: int = 7
    ) -> List[tuple]:
        """Aggressively split date range to ensure complete coverage."""
        ranges = []
        current_start = date_from
        current_days = initial_days

        while current_start < date_to:
            current_end = min(current_start + timedelta(days=current_days), date_to)
            ranges.append((current_start, current_end))
            current_start = current_end + timedelta(seconds=1)  # Avoid overlap

            # Reduce range if we're still hitting limits
            if current_days > self.MIN_DATE_RANGE_DAYS:
                current_days = max(self.MIN_DATE_RANGE_DAYS, current_days // 2)

        return ranges

    async def _search_vacancies_page(self, filters: VacancyFilters, page: int = 0) -> Dict[str, Any]:
        """Search vacancies for a specific page."""
        params = {
            'page': page,
            'per_page': self.MAX_RESULTS_PER_REQUEST,
        }

        # Add filters to parameters
        if filters.text:
            params['text'] = filters.text
        if filters.area:
            params['area'] = filters.area
        if filters.professional_role:
            params['professional_role'] = filters.professional_role
        if filters.industry:
            params['industry'] = filters.industry
        if filters.experience:
            params['experience'] = filters.experience.value
        if filters.employment:
            params['employment'] = filters.employment.value
        if filters.schedule:
            params['schedule'] = filters.schedule.value
        if filters.salary_from:
            params['salary'] = filters.salary_from
        if filters.currency:
            params['currency'] = filters.currency
        if filters.only_with_salary:
            params['only_with_salary'] = 'true'
        if filters.date_from:
            params['date_from'] = filters.date_from.strftime('%Y-%m-%dT%H:%M:%S')
        if filters.date_to:
            params['date_to'] = filters.date_to.strftime('%Y-%m-%dT%H:%M:%S')

        return await self._make_request('GET', '/vacancies', params=params)

    def _extract_salary_info(self, salary_data: Optional[Dict]) -> tuple:
        """Extract salary information and determine salary type."""
        if not salary_data:
            return None, None, None

        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency')

        # Determine salary type and value
        if salary_from and salary_to:
            salary_type_id = 3  # Range
            salary_value = (salary_from + salary_to) / 2  # Average
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
        # Extract salary information
        salary_type_id, salary_currency, salary_value = self._extract_salary_info(
            vacancy_data.get('salary')
        )

        # Get full vacancy details for description and contacts
        try:
            full_vacancy = await self.get_vacancy_details(vacancy_data['id'])
            description = full_vacancy.get('description', '')
            contacts = json.dumps(full_vacancy.get('contacts')) if full_vacancy.get('contacts') else None

            # Add small delay after getting details to prevent rate limiting
            await asyncio.sleep(0.2)  # 200ms delay after detail requests

        except Exception as e:
            self.logger.warning(f"Could not fetch full details for vacancy {vacancy_data['id']}: {e}")
            description = vacancy_data.get('snippet', {}).get('requirement', '')
            contacts = None

        return VacancyRecord(
            vacancy_id=None,  # Will be auto-generated in DB
            external_id=str(vacancy_data['id']),
            source_id=source_id,
            title=vacancy_data.get('name', ''),
            description=description,
            company_id=None,  # Would need separate company mapping
            salary_type_id=salary_type_id,
            salary_currency=salary_currency,
            salary_value=salary_value,
            experience_category_id=self._map_experience_to_category(vacancy_data.get('experience')),
            location_id=None,  # Would need separate location mapping
            specialization_id=vacancy_data.get('professional_roles', [{}])[0].get('id') if vacancy_data.get(
                'professional_roles') else None,
            published_at=vacancy_data.get('published_at'),
            contacts=contacts,
            url=vacancy_data.get('alternate_url')
        )

    async def search_all_vacancies(
            self,
            filters: VacancyFilters,
            max_results: Optional[int] = None
    ) -> AsyncGenerator[VacancyRecord, None]:
        """Search ALL vacancies using comprehensive strategy."""
        results_count = 0
        max_results = max_results or float('inf')

        # Set default date range if not provided
        if not filters.date_from or not filters.date_to:
            filters.date_to = datetime.now()
            filters.date_from = filters.date_to - timedelta(days=30)

        # Check if we need parameter-based splitting
        initial_response = await self._search_vacancies_page(filters, 0)
        total_found = initial_response.get('found', 0)

        self.logger.info(f"Total vacancies found: {total_found}")

        if total_found <= self.MAX_TOTAL_RESULTS:
            # Simple pagination is sufficient
            page = 0
            while results_count < max_results:
                response = await self._search_vacancies_page(filters, page)
                vacancies = response.get('items', [])
                if not vacancies:
                    break

                for vacancy in vacancies:
                    if results_count >= max_results:
                        return
                    if vacancy['id'] not in self.seen_vacancy_ids:
                        self.seen_vacancy_ids.add(vacancy['id'])
                        record = await self._convert_to_vacancy_record(vacancy)
                        yield record
                        results_count += 1

                if (page + 1) * self.MAX_RESULTS_PER_REQUEST >= min(total_found, self.MAX_TOTAL_RESULTS):
                    break
                page += 1
        else:
            # Need aggressive splitting strategy
            self.logger.info("Using aggressive splitting strategy")

            # First try date-based splitting
            date_ranges = self._split_date_range_aggressive(filters.date_from, filters.date_to)

            for date_from, date_to in date_ranges:
                if results_count >= max_results:
                    break

                date_filters = filters.copy()
                date_filters.date_from = date_from
                date_filters.date_to = date_to

                # Check if this date range still has too many results
                date_response = await self._search_vacancies_page(date_filters, 0)
                date_total = date_response.get('found', 0)

                if date_total <= self.MAX_TOTAL_RESULTS:
                    # Process this date range normally
                    page = 0
                    while results_count < max_results:
                        response = await self._search_vacancies_page(date_filters, page)
                        vacancies = response.get('items', [])
                        if not vacancies:
                            break

                        for vacancy in vacancies:
                            if results_count >= max_results:
                                return
                            if vacancy['id'] not in self.seen_vacancy_ids:
                                self.seen_vacancy_ids.add(vacancy['id'])
                                record = await self._convert_to_vacancy_record(vacancy)
                                yield record
                                results_count += 1

                        if (page + 1) * self.MAX_RESULTS_PER_REQUEST >= min(date_total, self.MAX_TOTAL_RESULTS):
                            break
                        page += 1
                else:
                    # Need parameter-based splitting
                    self.logger.info(
                        f"Date range {date_from} to {date_to} still has {date_total} results, using parameter splitting")

                    filter_combinations = self._create_filter_combinations(date_filters)

                    for combo_filters in filter_combinations:
                        if results_count >= max_results:
                            break

                        try:
                            page = 0
                            while results_count < max_results:
                                response = await self._search_vacancies_page(combo_filters, page)
                                vacancies = response.get('items', [])
                                if not vacancies:
                                    break

                                for vacancy in vacancies:
                                    if results_count >= max_results:
                                        return
                                    if vacancy['id'] not in self.seen_vacancy_ids:
                                        self.seen_vacancy_ids.add(vacancy['id'])
                                        record = await self._convert_to_vacancy_record(vacancy)
                                        yield record
                                        results_count += 1

                                combo_total = response.get('found', 0)
                                if (page + 1) * self.MAX_RESULTS_PER_REQUEST >= min(combo_total,
                                                                                    self.MAX_TOTAL_RESULTS):
                                    break
                                page += 1

                        except Exception as e:
                            self.logger.error(f"Error with filter combination: {e}")
                            continue

    async def get_vacancy_details(self, vacancy_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific vacancy."""
        return await self._make_request('GET', f'/vacancies/{vacancy_id}')


async def parse_and_save_vacancies_json(
        professional_roles: List[int],
        output_file: str = 'vacancies.json',
        max_results_per_role: Optional[int] = None,
        delay_between_roles: int = 10  # Increased default delay
):
    """Parse vacancies for multiple professional roles and save to JSON with enhanced rate limiting."""

    # Get credentials from environment variables
    client_id = os.getenv('HH_CLIENT_ID')
    client_secret = os.getenv('HH_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("HH_CLIENT_ID and HH_CLIENT_SECRET environment variables must be set")

    parser = HHAPIParser(
        client_id=client_id,
        client_secret=client_secret
    )

    all_vacancies = []
    failed_roles = []
    start_time = time.time()

    async with parser:
        for i, role_id in enumerate(professional_roles):
            try:
                logging.info(f"Processing role {i + 1}/{len(professional_roles)}: {role_id}")

                filters = VacancyFilters(
                    professional_role=role_id,
                    date_from=datetime.now() - timedelta(days=30),
                    date_to=datetime.now()
                )

                role_vacancies = []
                role_start_time = time.time()

                async for vacancy_record in parser.search_all_vacancies(filters, max_results_per_role):
                    role_vacancies.append(vacancy_record.to_dict())

                all_vacancies.extend(role_vacancies)

                role_elapsed = time.time() - role_start_time
                logging.info(f"Role {role_id} completed: {len(role_vacancies)} vacancies in {role_elapsed:.1f}s")
                logging.info(f"Total progress: {len(all_vacancies)} vacancies, {len(parser.seen_vacancy_ids)} unique")

                # Adaptive delay based on performance
                if role_elapsed < 30:  # If too fast, increase delay
                    delay = delay_between_roles * 1.5
                else:
                    delay = delay_between_roles

                logging.info(f"Waiting {delay}s before next role...")
                await asyncio.sleep(delay)

            except Exception as e:
                logging.error(f"Error processing role {role_id}: {e}")
                failed_roles.append(role_id)

                # Longer delay after error
                await asyncio.sleep(delay_between_roles * 2)
                continue

    # Final statistics
    total_elapsed = time.time() - start_time
    avg_rate = parser.request_count / total_elapsed if total_elapsed > 0 else 0

    logging.info(f"=== PARSING COMPLETED ===")
    logging.info(f"Total time: {total_elapsed / 3600:.1f} hours")
    logging.info(f"Total requests: {parser.request_count}")
    logging.info(f"Average rate: {avg_rate:.2f} req/s")
    logging.info(f"Total vacancies: {len(all_vacancies)}")
    logging.info(f"Unique vacancies: {len(parser.seen_vacancy_ids)}")
    logging.info(f"Failed roles: {len(failed_roles)} - {failed_roles}")

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_vacancies, f, ensure_ascii=False, indent=2, default=str)

    # Save failed roles for retry
    if failed_roles:
        with open('failed_roles.json', 'w') as f:
            json.dump(failed_roles, f, indent=2)

    logging.info(f"Results saved to {output_file}")
    return all_vacancies


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('vacancies_enhanced.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    test_roles = [44, 45, 46, 48, 144, 169, 174, 30, 47, 111, 112, 114, 96, 124]  # Engineer roles

    # Test run
    asyncio.run(parse_and_save_vacancies_json(
        test_roles,
        'test_vacancies.json',
        max_results_per_role=100,  # Limited for testing
        delay_between_roles=15  # Conservative delay for testing
    ))