import json
from typing import List, Optional, Dict, Any
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
import time
import random
from pydantic import BaseModel, ValidationError


class Salary(BaseModel):
    type: Optional[str] = None
    currency: Optional[str] = None
    value: Optional[int] = None


class Source(BaseModel):
    name: str


class ExperienceCategory(BaseModel):
    name: str


class Location(BaseModel):
    region: str


class Specialization(BaseModel):
    specialization: str


class EmploymentType(BaseModel):
    name: str


class TimeStamp(BaseModel):
    time_stamp: str


class Resume(BaseModel):
    id: int
    external_id: str
    source: Optional[Source] = None
    title: str
    salary: Salary
    description: Optional[str] = None
    location: Optional[Location] = None
    experience_category: Optional[ExperienceCategory] = None
    skills: Optional[str] = None
    education: Optional[str] = None
    specialization: Optional[Specialization] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    published_at: Optional[TimeStamp] = None


class ResumeParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.base_search_url = 'https://hh.ru/search/resume'
        self.session = requests.Session()
        self.source = Source(name="hh.ru")

    def parse_resume_page(self, url: str) -> Optional[Resume]:
        try:
            # Skip search pages - only parse actual resume pages
            if '/search/resume' in url:
                return None

            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # Extract basic info with fallbacks
            resume_id = url.split('/')[-1].split('?')[0]

            # Title is required - use multiple fallback strategies
            title = self._safe_extract(soup, 'h1', {'data-qa': 'resume-personal-name'})
            if not title:
                title = self._safe_extract(soup, 'div', {'data-qa': 'resume-block-title-position'})
            if not title:
                title = "Резюме без названия"

            # Description with fallback
            description = self._safe_extract(soup, 'div', {'data-qa': 'resume-block-experience'})
            if not description:
                description = self._safe_extract(soup, 'div', {'data-qa': 'resume-block-position'})

            # Salary with proper handling
            salary = self._parse_salary(soup)

            # Names with proper splitting
            first_name, last_name, middle_name = self._parse_personal_names(soup)

            # Create base resume with required fields
            resume_data = {
                'id': 0,  # Will be set by database
                'external_id': resume_id,
                'source': self.source,
                'title': title,
                'salary': salary,
                'description': description,
                'first_name': first_name,
                'last_name': last_name,
                'middle_name': middle_name,
                'published_at': TimeStamp(time_stamp=datetime.now().isoformat())
            }

            # Parse additional fields
            self._parse_location(soup, resume_data)
            self._parse_experience_category(soup, resume_data)
            self._parse_skills(soup, resume_data)
            self._parse_education(soup, resume_data)
            self._parse_specialization(soup, resume_data)

            try:
                return Resume(**resume_data)
            except ValidationError as e:
                print(f"Validation error for resume {url}: {e}")
                return None

        except Exception as e:
            print(f"Error parsing resume {url}: {e}")
            return None

    def _safe_extract(self, soup, tag, attrs) -> Optional[str]:
        element = soup.find(tag, attrs)
        return element.get_text(strip=True) if element else None

    def _parse_personal_names(self, soup) -> tuple:
        name_element = soup.find('h1', {'data-qa': 'resume-personal-name'})
        if not name_element:
            return (None, None, None)

        name_parts = name_element.get_text(strip=True).split()
        if len(name_parts) >= 2:
            last_name = name_parts[0]
            first_name = name_parts[1]
            middle_name = name_parts[2] if len(name_parts) > 2 else None
            return (first_name, last_name, middle_name)
        return (None, None, None)

    def _parse_salary(self, soup) -> Salary:
        salary_element = soup.find('span', {'data-qa': 'resume-block-salary'})
        if not salary_element:
            return Salary()

        salary_text = salary_element.get_text()
        match = re.search(r'(\d+[\s\d]*)\s*([₽€$₸])', salary_text.replace(' ', ''))
        if not match:
            return Salary()

        try:
            value = int(float(match.group(1)) * 100)  # Convert to fixed point
            currency = match.group(2)
            return Salary(value=value, currency=currency)
        except:
            return Salary()

    def _parse_location(self, soup, resume_data: dict):
        location_element = soup.find('span', {'data-qa': 'resume-personal-address'})
        if location_element:
            resume_data['location'] = Location(region=location_element.get_text(strip=True))

    def _parse_experience_category(self, soup, resume_data: dict):
        experience_element = soup.find('span', {'data-qa': 'resume-experience'})
        if experience_element:
            exp_text = experience_element.get_text(strip=True)
            if exp_text:
                resume_data['experience_category'] = ExperienceCategory(name=exp_text)

    def _parse_skills(self, soup, resume_data: dict):
        skills_block = soup.find('div', {'data-qa': 'resume-block-skills-content'})
        if skills_block:
            skills = [skill.get_text(strip=True) for skill in skills_block.find_all('span')]
            if skills:
                resume_data['skills'] = ', '.join(skills)

    def _parse_education(self, soup, resume_data: dict):
        education_block = soup.find('div', {'data-qa': 'resume-block-education'})
        if not education_block:
            return

        education_items = []
        items = education_block.find_all('div', {'data-qa': 'resume-block-education-item'})
        for item in items:
            institution = self._safe_extract(item, 'div', {'data-qa': 'resume-block-education-name'})
            faculty = self._safe_extract(item, 'div', {'data-qa': 'resume-block-education-faculty'})
            specialization = self._safe_extract(item, 'div', {'data-qa': 'resume-block-education-specialization'})
            year = self._safe_extract(item, 'div', {'data-qa': 'resume-block-education-year'})

            parts = []
            if institution:
                parts.append(institution)
            if faculty:
                parts.append(faculty)
            if specialization:
                parts.append(specialization)
            if year:
                parts.append(year)

            if parts:
                education_items.append(', '.join(parts))

        if education_items:
            resume_data['education'] = '; '.join(education_items)

    def _parse_specialization(self, soup, resume_data: dict):
        position_element = soup.find('div', {'data-qa': 'resume-block-position-position'})
        if position_element:
            specialization = position_element.get_text(strip=True)
            if specialization:
                resume_data['specialization'] = Specialization(specialization=specialization)

    def _filter_valid_resume_urls(self, urls: List[str]) -> List[str]:
        """Filter out search pages and invalid URLs"""
        return [
            url for url in urls
            if '/resume/' in url
               and not url.startswith('/search/resume')
               and len(url.split('/')[-1]) > 10  # Basic check for resume ID
        ]

    def search_resumes(self, query: str, area: int = 1, max_pages: int = 2) -> List[str]:
        """Search for resumes and return their URLs"""
        resume_urls = []

        for page in range(max_pages):
            params = {
                'text': query,
                'area': area,
                'page': page
            }

            try:
                response = self.session.get(self.base_search_url, params=params, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'lxml')

                links = soup.find_all('a', href=lambda href: href and '/resume/' in href)
                for link in links:
                    url = link['href'].split('?')[0]
                    if url.startswith('/'):
                        url = f'https://hh.ru{url}'
                    if url not in resume_urls:
                        resume_urls.append(url)

                time.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"Error searching resumes on page {page}: {e}")
                continue

        return self._filter_valid_resume_urls(resume_urls)

    def parse_resumes_to_json(self, query: str, output_file: str = 'resumes.json', max_resumes: int = 5):
        """Search for resumes, parse them and save to JSON file"""
        print(f"Searching for resumes with query: '{query}'")
        resume_urls = self.search_resumes(query, max_pages=2)
        valid_urls = self._filter_valid_resume_urls(resume_urls)
        print(f"Found {len(valid_urls)} valid resumes to parse")

        resumes = []
        for i, url in enumerate(valid_urls[:max_resumes]):
            print(f"Parsing resume {i + 1}/{len(valid_urls[:max_resumes])}: {url}")
            resume = self.parse_resume_page(url)
            if resume:
                resumes.append(json.loads(resume.json()))
            time.sleep(random.uniform(0.1, 0.3))

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resumes, f, ensure_ascii=False, indent=2)

        print(f"Saved {len(resumes)} resumes to {output_file}")
        return resumes


if __name__ == "__main__":
    parser = ResumeParser()
    resumes = parser.parse_resumes_to_json(
        query="Python разработчик",
        output_file="resumes.json",
        max_resumes=20
    )
    