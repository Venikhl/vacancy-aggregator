import os
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