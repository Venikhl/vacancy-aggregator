"""SuperJob API integration for fetching and processing job vacancy data asynchronously."""

import asyncio
import json
import os
from typing import List, Optional
import httpx
import aiofiles

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

default_catalogs = "33,35,66,71,427,433,276,626,329,336,347,351,481"

class SuperJobParser:
    """Class to handle asynchronous SuperJob API interactions and data processing."""

    def __init__(self):
        """Initialize the parser with an httpx AsyncClient and headers."""
        self.headers = {
            "X-Api-App-Id": (
                "v3.h.4904198.e970f48142f64d0607db3141b2cff0d185b18d90."
                "9f0484330b2780cd4b63fcb3b3f9b0fa4d482f33"
            ),
        }
        self.client = httpx.AsyncClient(timeout=10)

    async def close(self):
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

    async def all_vacancy_catalog(self):
        """Fetch and save all vacancies for the predefined catalogues."""
        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {
            "catalogues": default_catalogs,
            "count": 40,
        }
        response = await self.client.get(url, headers=self.headers, params=params)
        json_data = response.json()
        results = [json_data]
        total = json_data["total"]
        amount = total // 40
        for i in range(1, amount + 1):
            params["page"] = i
            response = await self.client.get(url, headers=self.headers, params=params)
            json_data = response.json()
            results.append(json_data)
        async with aiofiles.open("all_vacancy_catalog.json", "w", encoding="utf-8") as file:
            await file.write(json.dumps(results, ensure_ascii=False, indent=4))
            await file.write("\n")

    async def extract_data(self):
        """Load and return vacancy data from the saved JSON file."""
        async with aiofiles.open("all_vacancy_catalog.json", "r", encoding="utf-8") as file:
            content = await file.read()
            return json.loads(content)

    async def create_json_file(self, name: str, response: httpx.Response, mode: str = "a"):
        """Write the JSON response content to a file asynchronously."""
        json_content = response.json()
        full_path = os.path.join(script_dir, name)
        async with aiofiles.open(full_path, mode, encoding="utf-8") as json_file:
            await json_file.write(json.dumps(json_content, ensure_ascii=False, indent=4))

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
        response = await self.client.get(url, headers=self.headers, params=params)
        await self.create_json_file("response.json", response)
        return response.json()

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
        async with aiofiles.open("cleaned_catalog.json", "w", encoding="utf-8") as json_file:
            await json_file.write(json.dumps(parsed_cleaned, ensure_ascii=False, indent=4))

async def main():
    """Entry point for asynchronous script execution."""
    parser = SuperJobParser()
    try:
        await parser.all_vacancy_catalog()
    finally:
        await parser.close()

if __name__ == "__main__":
    asyncio.run(main())