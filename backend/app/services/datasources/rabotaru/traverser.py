"""Traversal and parsing logic for rabota.ru vacancy listings."""

import re
from typing import Iterable, List, Optional
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

from app.api.v1.models import Salary, VacancyShort
from app.services.datasources.rabotaru._api import _fetch


class VacancyShortWithUrl(VacancyShort):
    """Extension of VacancyShort model with URL field."""

    url: str


def _build_url(
    *,
    page: int,
    specialization_ids: Iterable[int] | None,
    industry_ids: Iterable[int],
    all_regions: bool,
) -> str:
    if not all_regions:
        raise NotImplementedError("all_regions=False is not supported yet")

    q = {"sort": "relevance", "page": str(page), "all_regions": "1"}
    if specialization_ids:
        q["specialization_ids"] = ",".join(map(str, specialization_ids))

    if industry_ids:
        q["industry_ids"] = ",".join(map(str, industry_ids))

    qs = "&".join(f"{k}={v}" for k, v in q.items())
    return f"https://www.rabota.ru/vacancy/?{qs}"


def _parse_salary(raw: str) -> Salary:
    """Parse string with salary from a div from a search page."""
    raw = raw.strip()

    # “От 80 тыс рублей” → value = 80 000 * 100 = 8 000 000
    m = re.search(r"(\d[\d\s]*)", raw)
    amount = (
        int(m.group(1).replace(" ", "").replace("\xa0", "")) * 100
        if m
        else None
    )

    return Salary(
        type=(
            "from"
            if raw.lower().startswith("от")
            else "to" if raw.lower().startswith("до") else None
        ),
        currency="RUB" if "руб" in raw.lower() else None,
        value=amount,
    )


def parse_vacancies(
    html: str, base_url: str = "https://www.rabota.ru"
) -> list[VacancyShort]:
    """Parse a rabota.ru vacancy.

    Search HTML page and extract top-level vacancy data.

    Extracted fields per vacancy:
    - ID: parsed from the numeric part of the <a href> link
    (e.g., /vacancy/53515632/)
    - Title: vacancy name from the anchor text
    - Description: short description from the
    `.vacancy-preview-card__description` div
    - Salary: parsed from the `.vacancy-preview-card__salary*` div

    Args:
        html: Raw HTML content of a vacancy list page.
        base_url: Base URL to resolve relative links

    Returns:
        A list of `VacancyShortWithUrl` models parsed from the page.
        Returns an empty list if no valid vacancies are found.
    """
    soup = BeautifulSoup(html, "lxml")
    out: list[VacancyShortWithUrl] = []

    for card in soup.select("div.vacancy-preview-card__top"):
        # title + link
        a = card.select_one("a.vacancy-preview-card__title_border")
        if not a or not a.get("href"):
            continue  # skip corrupt card
        href_abs = urljoin(base_url, a["href"])
        cleaned_url = href_abs.partition("/?")[0]

        title = a.get_text(strip=True)
        # id is the second path segment: /vacancy/53515632/…
        parts = urlparse(href_abs).path.strip("/").split("/")
        if len(parts) < 2 or not parts[1].isdigit():
            continue
        vac_id = int(parts[1])

        # description
        desc_tag = card.select_one("div.vacancy-preview-card__description")
        description = desc_tag.get_text(" ", strip=True) if desc_tag else None

        # salary (class name sometimes varies, so prefix match)
        sal_tag = card.select_one('[class*="vacancy-preview-card__salary"]')
        salary = (
            _parse_salary(sal_tag.get_text(" ", strip=True))
            if sal_tag
            else Salary()
        )

        out.append(
            VacancyShortWithUrl(
                id=vac_id,
                title=title,
                description=description,
                salary=salary,
                url=cleaned_url,
            )
        )
    return out


async def traverse(
    *,
    specialization_ids: Optional[List[int]] = None,
    industry_ids: List[int] = [1],
    all_regions: bool = True,
    limit: Optional[int] = None,  # total vacancies desired
    start_page: int = 1,
    page_limit: int = 10,  # max pages to walk
) -> List[VacancyShortWithUrl]:
    """
    Crawl rabota.ru.

    Search pages sequentially (async I/O) and return up to *limit*
    VacancyShort objects.

    Stops earlier if an empty result page is met.

    Stops earlier if exceeded the limit. May return list bigger than limit.
    """
    vacancies: list[VacancyShortWithUrl] = []
    if limit is not None and limit <= 0:
        return vacancies

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:  # rabota uses TLS-ALPN
        for page in range(start_page, start_page + page_limit):
            url = _build_url(
                page=page,
                specialization_ids=specialization_ids or [],
                industry_ids=industry_ids,
                all_regions=all_regions,
            )
            html = await _fetch(session, url)
            chunk = parse_vacancies(html)
            if not chunk:  # reached last page
                break

            vacancies.extend(chunk)
            if limit and len(vacancies) >= limit:
                return vacancies

    return vacancies
