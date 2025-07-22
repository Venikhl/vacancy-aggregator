"""
SuperJob API integration for fetching and processing job vacancy.

data asynchronously.
"""
import time
import asyncio
import hashlib
import json
import os
from typing import List, Optional, Dict, Any, AsyncGenerator
import httpx
import aiofiles
import hashlib
from playwright.async_api import async_playwright
from api.v1.models import Resume, Salary, Source, Location, ExperienceCategory
import re
script_dir = os.path.dirname(os.path.abspath(__file__))

catalog_dict = {
    33: "IT, Интернет, связь, телеком",
    35: "Web-дизайн (UI/UX)",
    66: "Графический дизайн",
    71: "Промышленный дизайн",
    427: "IT-консалтинг",
    433: "Управление проектами",
    276: "Инновационные технологии",
    626: "HR - хаб",
    329: "Авиационная промышленность",
    336: "Машиностроение, станкостроение",
    347: "Радиотехническая и электронная промышленность",
    351: "Робототехника",
    481: "Топ-персонал IT, Интернет, связь, телеком",
}
specializations = [
    "программист",
    "разработчик Golang",
    "frontend-разработчик",
    "backend-разработчик",
    "разработчик JavaScript",
    "разработчик мобильных приложений",
    "инженер-программист",
    "инженер по робототехнике",
    "разработчик алгоритмов для роботов",
    "data scientist",
    "системный аналитик",
    "интернет-маркетолог",
    "smm-менеджер",
    "web-дизайнер",
    "UX-дизайнер",
    "devops-инженер",
    "администратор IT-систем",
    "архитектор баз данных",
    "разработчик баз данных",
    "специалист по ERP-системам",
    "it-менеджер",
    "HR-специалист в IT",
    "менеджер по продукту",
    "PR-менеджер",
    "блогер в IT"
]

default_catalogs = "33,35,66,71,427,433,276,626,329,336,347,351,481"


class SuperJobParser(VacancyParser):
    """Handle asynchronous SuperJob API interactions and data processing."""

    def __init__(self,  config: Optional[ParserConfig] = None,):
        """Initialize the parser with an httpx AsyncClient and headers."""
        self.headers = {
            "X-Api-App-Id": (
                "v3.h.4904198.e970f48142f64d0607db3141b2cff0d185b18d90."
                "9f0484330b2780cd4b63fcb3b3f9b0fa4d482f33"
            ),
        }
        self.client = httpx.AsyncClient(timeout=10)

        super().__init__(config or ParserConfig())

    @property
    def parser_name(self) -> str:
        """Return the name of the parser."""
        return "superjob_parser"

    @property
    def source_name(self) -> str:
        """Return the name of the data source."""
        return "superjob.ru"

    async def parse_and_save(
        self,
        filters: Optional[VacancyFilter] | None,
        max_results: Optional[int] = None
    ) -> ParserResult:
        """Parse vacancies and save it to JSON file."""
        start_time = datetime.now()
        output_file = self._generate_output_filename(filters)

        self.logger.info(f"Starting {self.parser_name} parsing...")
        url = "https://api.superjob.ru/2.0/vacancies/"

        """Fetch and save all vacancies for the predefined catalogues."""
        params = {
            "catalogues": default_catalogs,
            "count": 40,
            "town": filters.location.region,
            "payment_from": filters.salary_min,
            "payment_to": filters.salary_max,
            "experience": filters.experience_categories[0].years_of_experience,
            "date_published_from": filters.date_published_from,
            "date_published_to": filters.date_published_to
        }
        response = await self.client.get(url, headers=self.headers,
                                         params=params)
        json_data = response.json()
        results = [json_data]
        total = json_data["total"]
        amount = total // 40
        for i in range(1, amount + 1):
            params["page"] = i
            response = await self.client.get(url, headers=self.headers,
                                             params=params)
            json_data = response.json()
            results.append(json_data)
        async with aiofiles.open(output_file, "a",
                                 encoding="utf-8") as file:
            await file.write(json.dumps(results, ensure_ascii=False, indent=4))
            await file.write("\n")
        self.logger.info(f"Saved {len(results)} vacancies to {output_file}")
        processing_time = (datetime.now() - start_time).total_seconds()
        result = ParserResult(
            parser_name=self.parser_name,
            total_vacancies=len(results),
            unique_vacancies=len(self.seen_vacancy_ids),
            output_file=output_file,
            processing_time=processing_time,
            errors=self.errors.copy(),
            metadata={
                "filters": filters,
                "max_results": total,
                "timestamp": start_time.isoformat
            }
        )
        self.logger.info(
            f"Parsing completed: {len(results)}"
            f"vacancies saved to {output_file}"
        )
        return result

    async def cleanup(self):
        """Close the httpx AsyncClient."""
        await self.client.aclose()

    async def vacancy_catalog(self):
        """Fetch and save the full catalog from SuperJob API."""
        url = "https://api.superjob.ru/2.0/catalogues/"
        response = await self.client.get(url)
        await self.create_json_file("catalog.json", response, mode="w")

    async def choose_catalogues(self) -> List[int]:
        """Return predefined catalogues (user input replaced with default)."""
        for key, value in catalog_dict.items():
            print(key, value)
        return [int(c) for c in default_catalogs.split(",")]

    async def extract_data(self):
        """Load and return vacancy data from the saved JSON file."""
        async with aiofiles.open("all_vacancy_catalog.json", "r",
                                 encoding="utf-8") as file:
            content = await file.read()
            return json.loads(content)

    async def create_json_file(self, name: str,
                               response: httpx.Response, mode: str = "a"):
        """Write the JSON response content to a file asynchronously."""
        json_content = response.json()
        full_path = os.path.join(script_dir, name)
        async with aiofiles.open(full_path, mode,
                                 encoding="utf-8") as json_file:
            await json_file.write(json.dumps(json_content,
                                             ensure_ascii=False, indent=4))

    async def find_vacancies(
        self,
        keyword: Optional[str] = None,
        published_all: bool = True,
        type_of_work: Optional[str] = None,
        period: int = 7,
        catalogues: Optional[str] = None,
        town: Optional[str] = None,
        experience: Optional[str] = None,
        payment_from: Optional[int] = None,
        payment_to: Optional[int] = None,
    ):
        """Search for vacancies with filters and save the result to a file."""
        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {
            "keyword": keyword,
            "published_all": published_all,
            "type_of_work": type_of_work,
            "period": period,
            "catalogues": catalogues,
            "town": town,
            "experience": experience,
            "payment_from": payment_from,
            "payment_to": payment_to,
        }
        response = await self.client.get(url, headers=self.headers,
                                         params=params)
        await self.create_json_file("response.json", response)
        return response.json()

    def _convert_to_vacancy_model(self, raw_data: Dict[str, Any]) -> Vacancy:
        """Convert raw API data to Vacancy model."""
        pass

    async def get_vacancy_details(self, external_id: str) -> Optional[Vacancy]:
        """Get detailed information about a specific vacancy."""
        pass

    async def search_vacancies(
        self,
        filters: VacancyFilter,
        max_results: Optional[int] = None
    ) -> AsyncGenerator[Vacancy, None]:
        """Search vacancies with given filters, yielding each vacancy."""
        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {
            "catalogues": default_catalogs,
            "count": 40,
            "town": filters.location.region,
            "payment_from": filters.salary_min,
            "payment_to": filters.salary_max,
            "experience": filters.experience_categories[0].years_of_experience,
            "date_published_from": filters.date_published_from,
            "date_published_to": filters.date_published_to
        }

        response = await self.client.get(
            url, headers=self.headers, params=params)
        json_data = response.json()
        total = json_data["total"]
        amount = total // 40 + (1 if total % 40 else 0)

        yielded_count = 0

        for page_num in range(amount):
            if max_results is not None and yielded_count >= max_results:
                break

            params["page"] = page_num
            response = await self.client.get(
                url, headers=self.headers, params=params)
            json_data = response.json()

            for vacancy_data in json_data["objects"]:
                if max_results is not None and yielded_count >= max_results:
                    break

                try:
                    company_name = vacancy_data["client"]["title"]
                except (KeyError, TypeError):
                    company_name = None

                vacancy = Vacancy(
                    id=vacancy_data["id"],
                    external_id=vacancy_data["id_client"],
                    source=Source(name=vacancy_data["link"]),
                    title=vacancy_data["profession"],
                    description=vacancy_data["vacancyRichText"],
                    company=Company(name=company_name),
                    salary=Salary(
                        currency=vacancy_data["currency"],
                        type=vacancy_data["currency"],
                        value=vacancy_data["payment_to"]
                    ),
                    experience_category=ExperienceCategory(
                        name=vacancy_data["experience"]["title"],
                        years=vacancy_data["experience"]["title"]
                    ),
                    location=Location(region=vacancy_data["town"]["title"]),
                    specialization=Specialization(
                        specialization=vacancy_data["profession"]),
                    employment_types=[EmploymentType(
                        name=vacancy_data["type_of_work"]["title"])],
                    published_at=TimeStamp(
                        time_stamp=vacancy_data["date_published"]),
                    contacts=vacancy_data["phone"],
                    url=vacancy_data["link"]
                )
                yield vacancy
                yielded_count += 1

    async def parse_catalog_cleaned(self):
        """Fetch, clean, and store a simplified version of the catalogues."""
        url = "https://api.superjob.ru/2.0/catalogues/"
        response = await self.client.get(url)
        json_data = response.json()
        parsed_cleaned = []
        for item in json_data:
            positions = [
                {
                    "title_ru": p["title_rus"],
                    "key": p["key"],
                    "id_parent": p["id_parent"],
                }
                for p in item["positions"]
            ]
            parsed_cleaned.append(
                {
                    "title_rus": item["title_rus"],
                    "key": item["key"],
                    "positions": positions,
                }
            )
        async with aiofiles.open("cleaned_catalog.json",
                                 "w", encoding="utf-8") as json_file:
            await json_file.write(json.dumps(parsed_cleaned,
                                             ensure_ascii=False, indent=4))

class ResumeScraping:
    base_url = "https://www.superjob.ru/resume/"

    def __init__(self, speciality_name, amount):
        self.speciality_name = speciality_name
        self.amount = amount

    async def scrape(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(self.base_url)
            await page.fill('input[name="keywords"]', self.speciality_name)
            await page.click('button#searchByHintSelect-input')
            await page.click('text=Резюме')
            await page.click('button[type="submit"]')
            current_url = page.url
            print(current_url)
            await asyncio.sleep(3)

<<<<<<< HEAD
            await asyncio.sleep(5)

            page_link_elements = await page.query_selector_all('a[class*="f-test-link-"][title]:not([title="дальше"])')


=======
            page_link_elements = await page.query_selector_all('a[class*="f-test-link-"][title]:not([title="дальше"])')

>>>>>>> d19142b (feat(resume):  added scraping of all search results)
            max_page_number = 1

            if page_link_elements:
                page_numbers = []
                for element in page_link_elements:
                    title = await element.get_attribute('title')
                    if title and title.isdigit():
                        page_numbers.append(int(title))

                if page_numbers:
                    max_page_number = max(page_numbers)

            print(f"Total pages found: {max_page_number}")

            all_scraped_data = []

            for i in range(1, min(max_page_number + 1, self.amount + 1)):
                print(f"Scraping page {i}...")
<<<<<<< HEAD
                if i > 1:
                    next_page_selector = f'a[title="{i}"]'
                    await page.click(next_page_selector)
                    await asyncio.sleep(5)


                # job_listings = await page.query_selector_all('div.f-test-search-result-item')
                # job_listings = await page.query_selector_all('div._1-PID._3LfUi.URBLZ')
=======
                if i >= 1:
                    next_page_selector = current_url+f"&page={i}"
                    print(next_page_selector)
                    await page.goto(next_page_selector)
                    await asyncio.sleep(2)

>>>>>>> d19142b (feat(resume):  added scraping of all search results)
                job_listings = await page.query_selector_all('div.f-test-search-result-item')
                links = []
                for i in job_listings:
                    link_element = await i.query_selector('a[target="_blank"]')
                    link = await link_element.get_attribute('href') if link_element else None
                    if link:
                        links.append("https://www.superjob.ru" + link)
                for link in links:
                    try:
                        await page.goto(link)
                        job_title = await page.locator('h1.VB8-V._3R5DT._3doCL.eFbGk').text_content()
                        salary = await page.locator('span._3R5DT._3doCL._1taY2').first.text_content()
                        try:
                            amount = int(re.sub(r'[^\d]', '', salary))
                            currency = re.sub(
                                r'[\d\s\xa0]', '', salary).strip()
                        except ValueError:
                            amount = 0
                            currency = salary
                        salary_information = Salary(
                            type=currency, currency=currency, value=amount)
                        source = Source(name=link)

                        age_info = await page.locator('span._1un4T.X9SAU.Xu7gX._1lLeK._2GB-\\_._3doCL._2k8ZM.rtYnN').inner_text()

                        loc = await page.locator('div.J\\+R2u').text_content()
                        loc = loc.replace('\xa0', ' ')
                        location = Location(region=loc)
                        work_experience = await page.locator("h2.j66yb:has-text('Опыт работы')").text_content()
                        work_experience = work_experience.replace('\xa0', ' ')
                        integers = re.findall(r'\d+', work_experience)

                        years_of_experience = int(
                            integers[0]) if integers else 0
                        exp_cat = ExperienceCategory(
                            name=work_experience, years_of_experience=years_of_experience)

                        employment = await page.locator('div.MokF1 span._1taY2:has-text("Занятость")').text_content()
                        citizenship_label = page.locator(
                            'div:has-text("Гражданство")')
                        citizenship_value = citizenship_label.locator(
                            'xpath=following-sibling::div[1]/span').first
                        citizenship = await citizenship_value.text_content()

                        resume = Resume(
                            id=int(hashlib.md5(link.encode()).hexdigest(), 16),
                            external_id=link.split(
                                "/")[-2] if link != 'N/A' else "unknown",
                            source=source,
                            title=job_title,
                            salary=salary_information,
                            location=location,
                            age_info=age_info,
                            experience_category=exp_cat,
                            citizenship=citizenship,
                            employment=employment
                        )
                        # scraped_item = {
                        #     "Education": education_list,
                        #     "Foreign Languages": languages,
                        #     "Driver's License": license_category
                        # }
                        all_scraped_data.append(resume)
                    except Exception as e:
                        print(f"Error scraping a job listing: {e}")
                        continue

                if len(all_scraped_data) >= self.amount:
                    print(
                        f"Reached desired amount of {self.amount} items. Stopping scrape.")
                    break

            await browser.close()
            print("Here: \n", all_scraped_data)
        return all_scraped_data

<<<<<<< HEAD
=======
           
>>>>>>> d19142b (feat(resume):  added scraping of all search results)
async def main():
    """Entry point for asynchronous script execution."""
    config = ParserConfig(
        max_results_per_batch=100,
        delay_between_requests=0.2,
        output_directory="parsed_data"
    )
    parser = SuperJobParser(config)
    try:
        # last 30 days
        date_to = datetime.now()
        date_from = date_to - timedelta(days=30)
        vf = VacancyFilter(title="all", salary_min=0, salary_max=99999,
                           experience_categories=[
                               ExperienceCategory(name="all",
                                                  years_of_experience=0)],
                           location=Location(region="Москва"),
                           date_published_from=int(date_from.timestamp()),
                           date_to=int(date_to.timestamp()))
        await parser.search_vacancies(filters=vf)
        await parser.parse_and_save(filters=vf)
    finally:

        await parser.cleanup()
    start_time = time.time()
    all_scraped_specializations = []
    for i in specializations:
        scraper = ResumeScraping(i)
        all_scraped_specializations.append(await scraper.scrape())
    end_time = time.time()
    result = end_time-start_time
    print(result, "\n", result/60)


if __name__ == "__main__":
    asyncio.run(main())
