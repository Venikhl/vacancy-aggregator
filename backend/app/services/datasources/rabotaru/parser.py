from bs4 import BeautifulSoup, NavigableString
import re
import aiohttp

from app.api.v1.models import (
    TimeStamp,
    VacancyShort,
    Vacancy,
    Location,
    EmploymentType,
    Company,
    Source,
    ExperienceCategory,
)

from app.services.datasources.rabotaru._api import _fetch
from app.services.datasources.rabotaru.traverser import VacancyShortWithUrl

SOURCE = "rabota.ru"


async def parse_vacancy(short: VacancyShort, url: str | None = None) -> Vacancy:
    if isinstance(short, VacancyShortWithUrl):
        url = short.url
    elif url is None:
        raise TypeError("No url")

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:  # rabota uses TLS-ALPN
        html = await _fetch(session, url)

    description = extract_markdown_description(html)
    region = extract_city_name(html)
    company = extract_company_name(html)
    time_stamp = extract_date(html)
    experience, education, employment = extract_experience_education_employment(html)

    if education:
        description = education + "\n\n" + description

    return Vacancy(
        id=-1,
        external_id=str(short.id),
        source=Source(name=SOURCE),
        title=short.title,
        description=description,
        company=Company(name=company) if company else None,
        salary=short.salary,
        experience_category=ExperienceCategory(name=experience) if experience else None,
        location=Location(region=region) if region else None,
        specialization=None,
        employment_types=[EmploymentType(name=employment)] if employment else [],
        published_at=TimeStamp(time_stamp=time_stamp) if time_stamp else None,
        contacts=None,
        url=url,
    )


# --- Helper parser functions ---


def extract_markdown_description(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    description_div = soup.find("div", itemprop="description")

    markdown = []
    for tag in description_div.children:
        if tag.name == "p":
            text = tag.get_text(strip=True)
            if text:
                markdown.append(f"\n## {text}\n")
        elif tag.name == "ul":
            for li in tag.find_all("li"):
                markdown.append(f"- {li.get_text(strip=True)}")
    result = "\n".join(markdown)

    skills = skills_to_markdown(extract_required_skills(html))

    if skills:
        result += "\n\n" + skills

    address = extract_address(html)

    if address:
        result += "\n\n" + address

    return result


def extract_required_skills(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")

    skills_container = soup.find("div", class_="vacancy-card__skills-list")
    if not skills_container:
        return []

    skills = [
        item.get_text(strip=True)
        for item in skills_container.find_all("div", class_="vacancy-card__skills-item")
    ]

    return skills


def skills_to_markdown(skills: list[str] | None) -> str:
    if not skills:
        return ""
    md = "### Необходимые навыки:\n"
    for skill in skills:
        md += f"- {skill}\n"
    return md


def extract_company_name(html: str) -> str | None:
    """Extract company name from <a> tag inside <div class="vacancy-company-stats__name">."""
    soup = BeautifulSoup(html, "lxml")
    div = soup.find("div", class_="vacancy-company-stats__name")
    if not div:
        return None

    a_tag = div.find("a")
    return a_tag.get_text(strip=True) if a_tag else None


def extract_city_name(html: str) -> str | None:
    """Extract city name from <span class="vacancy-requirements__city">."""
    soup = BeautifulSoup(html, "lxml")
    span = soup.find("span", class_="vacancy-requirements__city")
    return span.get_text(strip=True).strip(",.\n ") if span else None


def _extract_additional_requirements(html: str) -> str | None:
    """
    Extract additional requirements text that follows
    <span class="vacancy-requirements__city"> in the same parent.
    """
    soup = BeautifulSoup(html, "lxml")
    city_span = soup.find("span", class_="vacancy-requirements__city")
    if not city_span:
        return None

    sibling = city_span.find_next_sibling("span")
    return sibling.get_text(strip=True) if sibling else None


def extract_experience_education_employment(
    html: str,
) -> tuple[str | None, str | None, str | None]:
    req = _extract_additional_requirements(html)

    experience = education = employment = None

    match req.split(","):
        # 'опыт работы не имеет значения, образование любое'
        case experience, education:
            experience = experience
            education = education
        # полный день, опыт работы от 3 лет, образование среднее профессиональное
        case employment, experience, education:
            employment = employment
            experience = experience
            education = education

        # never seen this but what if
        case singe_string,:
            if "опыт" in singe_string:
                experience = singe_string
            if "образование" in singe_string:
                education = singe_string
        case _:
            pass

    return experience, education, employment


def extract_address(html: str) -> str | None:
    """
    Extract text from <div itemprop="address" class="vacancy-locations__address">,
    excluding child elements like .vacancy-locations__stations.
    """
    soup = BeautifulSoup(html, "lxml")
    address_div = soup.find(
        "div", itemprop="address", class_="vacancy-locations__address"
    )
    if not address_div:
        return None

    for content in address_div.contents:
        if isinstance(content, NavigableString):
            text = content.strip()
            if text:
                return text
    return None


def extract_date(html: str) -> str | None:
    """
    Extract date from <span class="vacancy-system-info__updated-date">.
    Prefer <meta itemprop="datePosted"> if available, else take the second <span>.
    """
    soup = BeautifulSoup(html, "lxml")
    wrapper = soup.find("span", class_="vacancy-system-info__updated-date")
    if not wrapper:
        return None

    meta = wrapper.find("meta", itemprop="datePosted")
    if meta and meta.has_attr("content"):
        return meta["content"]

    spans = wrapper.find_all("span")
    if len(spans) >= 2:
        return spans[1].get_text(strip=True)

    return None


def parse_vacancy_phones(html: str) -> str:
    raise NotImplementedError

    # need to click, without clicking this return empty string

    soup = BeautifulSoup(html, "lxml")

    # 1. Locate the vacancy-phones container
    container = soup.find("div", class_=re.compile(r"\bvacancy-phones\b"))
    if not container:
        return ""

    # 2. Remove unwanted "spam" sections
    for unwanted in container.select(
        ".vacancy-phones__mini-description, "  # disclaimer block
        ".vacancy-phones__sub-content-row_comment"  # sub-comments like timing
    ):
        unwanted.decompose()

    # 3. Extract and combine all remaining text
    text = container.get_text(separator=" ", strip=True)
    return text
