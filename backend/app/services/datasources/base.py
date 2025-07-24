"""Abstract base classes for parsers with unified interfaces."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime
import json
import logging
import os
from dataclasses import dataclass, field
from app.api.v1.models import (
    Vacancy, VacancyFilter, Source, Salary,
    ExperienceCategory, Location, Specialization,
    EmploymentType, TimeStamp, ResumeFilter,
    Resume
)


@dataclass
class ParserConfig:
    """Configuration for parsers."""

    max_results_per_batch: int = 100
    delay_between_requests: float = 1.0
    output_directory: str = "parsed_data"
    log_level: str = "INFO"
    timeout: int = 30
    retry_attempts: int = 3

    def __post_init__(self):
        """Create output directory if it doesn't exist."""
        os.makedirs(self.output_directory, exist_ok=True)


@dataclass
class ParserResult:
    """Result of parsing operation."""

    parser_name: str
    total_vacancies: int
    unique_vacancies: int
    output_file: str
    processing_time: float
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseParser(ABC):
    """Abstract base class for all parsers."""

    def __init__(self, config: ParserConfig):
        """Initialize parser with configuration."""
        self.config = config
        self.logger = self._setup_logger()
        self.seen_ids: set = set()
        self.errors: List[str] = []

    def _setup_logger(self) -> logging.Logger:
        """Set up logger for the parser."""
        logger = logging.getLogger(f"{self.__class__.__name__}")
        logger.setLevel(getattr(logging, self.config.log_level))

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @property
    @abstractmethod
    def parser_name(self) -> str:
        """Return the name of the parser."""
        pass

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of the data source."""
        pass

    @abstractmethod
    async def cleanup(self):
        """Cleanup resources (close connections, etc.)."""
        pass

    def _generate_output_filename(self, filters: Any, prefix: str = "") -> str:
        """Generate output filename based on filters and timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filter_part = ""

        if hasattr(filters, 'title') and filters.title:
            filter_part = f"_{filters.title.replace(' ', '_')}"

        filename = f"{self.parser_name}_{timestamp}{prefix}{filter_part}.json"
        return os.path.join(self.config.output_directory, filename)

    async def _save_to_json(
            self, data: List[Dict], filename: str, data_type: str):
        """Save data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            self.logger.info(f"Saved {len(data)} {data_type} to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {e}")
            raise

    def create_source(self, source_id: int = 1) -> Source:
        """Create Source model instance."""
        return Source(name=self.source_name)

    def create_salary(
        self,
        salary_type: str = None,
        currency: str = None,
        value: int = None
    ) -> Salary:
        """Create Salary model instance."""
        return Salary(type=salary_type, currency=currency, value=value)

    def create_experience_category(self, name: str) -> ExperienceCategory:
        """Create ExperienceCategory model instance."""
        return ExperienceCategory(name=name)

    def create_location(self, region: str) -> Location:
        """Create Location model instance."""
        return Location(region=region)

    def create_specialization(self, specialization: str) -> Specialization:
        """Create Specialization model instance."""
        return Specialization(specialization=specialization)

    def create_employment_type(self, name: str) -> EmploymentType:
        """Create EmploymentType model instance."""
        return EmploymentType(name=name)

    def create_timestamp(self, timestamp: str) -> TimeStamp:
        """Create TimeStamp model instance."""
        return TimeStamp(time_stamp=timestamp)


class VacancyParser(BaseParser):
    """Abstract base class for all vacancy parsers."""

    def __init__(self, config: ParserConfig):
        """Initialize the vacancy parser with configuration.

        Args:
            config (ParserConfig): Parser configuration settings.
        """
        super().__init__(config)
        self.seen_vacancy_ids: set = set()

    @abstractmethod
    async def search_vacancies(
        self,
        filters: VacancyFilter,
        max_results: Optional[int] = None
    ) -> AsyncGenerator[Vacancy, None]:
        """Search vacancies with given filters."""
        pass

    @abstractmethod
    async def get_vacancy_details(self, external_id: str) -> Optional[Vacancy]:
        """Get detailed information about a specific vacancy."""
        pass

    @abstractmethod
    def _convert_to_vacancy_model(self, raw_data: Dict[str, Any]) -> Vacancy:
        """Convert raw API data to Vacancy model."""
        pass

    async def parse_and_save(
        self,
        filters: VacancyFilter | None,
        max_results: Optional[int] = None
    ) -> ParserResult:
        """Parse vacancies and save it to JSON file."""
        start_time = datetime.now()
        output_file = self._generate_output_filename(filters)
        vacancies = []

        self.logger.info(f"Starting {self.parser_name} parsing...")

        try:
            async for vacancy in self.search_vacancies(filters, max_results):
                if vacancy.external_id not in self.seen_ids:
                    self.seen_ids.add(vacancy.external_id)
                    vacancies.append(vacancy.dict())

                    if len(vacancies) % 100 == 0:
                        self.logger.info(f"Collected "
                                         f"{len(vacancies)} vacancies...")

            await self._save_to_json(vacancies, output_file, "vacancies")

            processing_time = (datetime.now() - start_time).total_seconds()

            return ParserResult(
                parser_name=self.parser_name,
                total_vacancies=len(vacancies),
                unique_vacancies=len(self.seen_ids),
                output_file=output_file,
                processing_time=processing_time,
                errors=self.errors.copy(),
                metadata={
                    "filters": filters.dict() if filters else None,
                    "max_results": max_results,
                    "timestamp": start_time.isoformat()
                }
            )

        except Exception as e:
            self.logger.error(f"Error during parsing: {e}")
            self.errors.append(str(e))
            raise



class ResumeParser(BaseParser):
    """Abstract base class for all resume parsers."""

    @abstractmethod
    async def search_resumes(
        self,
        filters: ResumeFilter,
        max_results: Optional[int] = None
    ) -> AsyncGenerator[Resume, None]:
        """Search resumes with given filters."""
        pass

    @abstractmethod
    async def get_resume_details(self, external_id: str) -> Optional[Resume]:
        """Get detailed information about a specific resume."""
        pass

    @abstractmethod
    def _convert_to_resume_model(self, raw_data: Dict[str, Any]) -> Resume:
        """Convert raw data to Resume model."""
        pass

    async def parse_and_save(
        self,
        filters: ResumeFilter | None,
        max_results: Optional[int] = None
    ) -> ParserResult:
        """Parse resumes and save to JSON file."""
        start_time = datetime.now()
        output_file = self._generate_output_filename(filters, "_resumes")
        resumes = []

        self.logger.info(f"Starting {self.parser_name} resume parsing...")

        try:
            async for resume in self.search_resumes(filters, max_results):
                if resume.external_id not in self.seen_ids:
                    self.seen_ids.add(resume.external_id)
                    resumes.append(resume.dict())

                    if len(resumes) % 100 == 0:
                        self.logger.info(f"Collected {len(resumes)} resumes...")

            await self._save_to_json(resumes, output_file, "resumes")

            processing_time = (datetime.now() - start_time).total_seconds()

            return ParserResult(
                parser_name=self.parser_name,
                total_vacancies=len(resumes),
                unique_vacancies=len(self.seen_ids),
                output_file=output_file,
                processing_time=processing_time,
                errors=self.errors.copy(),
                metadata={
                    "filters": filters.dict() if filters else None,
                    "max_results": max_results,
                    "timestamp": start_time.isoformat()
                }
            )

        except Exception as e:
            self.logger.error(f"Error during parsing: {e}")
            self.errors.append(str(e))
            raise


class ParserManager:
    """Manager class for handling multiple parsers."""

    def __init__(self, parsers: List[BaseParser]):
        """Initialize with list of parsers."""
        self.parsers = parsers
        self.logger = logging.getLogger(self.__class__.__name__)

    async def parse_all(
        self,
        filters: Any,
        max_results_per_parser: Optional[int] = None
    ) -> List[ParserResult]:
        """Parse data using all available parsers."""
        results = []

        for parser in self.parsers:
            try:
                self.logger.info(f"Starting {parser.parser_name} parser...")
                result = await parser.parse_and_save(
                    filters, max_results_per_parser)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error in {parser.parser_name}: {e}")
                continue

        return results

    async def parse_specific(
        self,
        parser_names: List[str],
        filters: Any,
        max_results_per_parser: Optional[int] = None
    ) -> List[ParserResult]:
        """Parse data using specific parsers."""
        results = []

        for parser in self.parsers:
            if parser.parser_name in parser_names:
                try:
                    result = await parser.parse_and_save(
                        filters, max_results_per_parser)
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error in {parser.parser_name}: {e}")
                    continue

        return results

    def get_parser_by_name(self, name: str) -> Optional[BaseParser]:
        """Get parser by name."""
        for parser in self.parsers:
            if parser.parser_name == name:
                return parser
        return None

    def list_parsers(self) -> List[str]:
        """List all available parser names."""
        return [parser.parser_name for parser in self.parsers]
