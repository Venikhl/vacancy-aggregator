"""SuperJob API integration for fetching and processing job vacancy data."""

import requests
import json
import os
from typing import List

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

catalogs = "33,35,66,71,427,433,276,626,329,336,347,351,481"
headers = {
    "X-Api-App-Id":
        "v3.h.4904198.e970f48142f64d0607db3141b2cff0d185b18d90."
        "9f0484330b2780cd4b63fcb3b3f9b0fa4d482f33",
}


def vacancy_catalog():
    """Fetch and save the full catalog from SuperJob API."""
    url = "https://api.superjob.ru/2.0/catalogues/"
    response = requests.get(url, timeout=10)
    create_json_file("catalog.json", response, mode='w')


def choose_catalogues() -> List[int]:
    """Prompt user to select catalogues from the predefined dictionary."""
    for key, value in catalog_dict.items():
        print(key, value)
    choise_input = input()
    return choise_input


def all_vacancy_catalog():
    """Fetch and save all vacancies for the predefined catalogues."""
    url = "https://api.superjob.ru/2.0/vacancies/"
    catalogs = "33,35,66,71,427,433,276,626,329,336,347,351,481"
    params = {
        "catalogues": catalogs,
        "count": 40,
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    json_data = json.loads(response.content.decode('utf-8'))
    results = []
    results.append(json_data)
    total = json_data['total']
    amount = total // 40
    for i in range(1, amount+1):
        response = requests.get(
            url, headers=headers, params=params, timeout=10)
        json_data = json.loads(response.content.decode('utf-8'))
        results.append(json_data)
    with open('all_vacancy_catalog.json', 'a') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
        file.write('\n')


def extract_data():
    """Load and return vacancy data from the saved JSON file."""
    name = 'all_vacancy_catalog.json'
    with open(name, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


def create_json_file(name, response, mode='a'):
    """Write the JSON response content to a file."""
    json_content = json.loads(response.content.decode('utf-8'))
    full_path = os.path.join(script_dir, name)
    with open(full_path, mode) as json_file:
        json.dump(json_content, json_file, ensure_ascii=False, indent=4)


def find_vacancies(
    keyword=None, published_all=True, type_of_work=None,
    period=7, catalogues=None, town=None, experience=None,
        payment_from=None, payment_to=None):
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
        "payment_to": payment_to
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    create_json_file('response.json', response)
    return json.loads(response.content.decode('utf-8'))


def main():
    """Entry point for script execution."""
    all_vacancy_catalog()


def test_parsing():
    """Download a sample of vacancies from the API for testing purposes."""
    for i in range(1, 10):
        url = (
            f"https://api.superjob.ru/2.0/vacancies/"
            f"?catalogues=(260, 306)&page={i}&count=40")
        resposne = requests.get(url, headers=headers, timeout=10)
        create_json_file('rubbish.json', resposne, mode='a')


def parse_catalog_cleaned():
    """Fetch, clean, and store a simplified version of the catalogues."""
    url = 'https://api.superjob.ru/2.0/catalogues/'
    parsed__cleaned = []
    response = requests.get(url, timeout=10)
    json_data = response.json()
    for i in json_data:
        positions = []
        for p in i['positions']:
            positions.append({
                "title_ru": p['title_rus'],
                "key": p["key"],
                "id_parent": p['id_parent']})
        parsed__cleaned.append({
            "title_rus": i["title_rus"],
            "key": i["key"],
            "positions": positions})
    with open("cleaned_catalog.json", "w") as json_file:
        json.dump(parsed__cleaned, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
