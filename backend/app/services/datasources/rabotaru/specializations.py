import json
from pydantic import BaseModel

CATALOG_PATH = "app/services/datasources/rabotaru/catalog.json"

IT_SPECIALIZATIONS = [
    "программист",
    "web-программист",
    "программист python",
    "разработчик Golang",
    "инженер-разработчик",
    "программист java",
    "devops",
    "Data Scientist",
    "дизайнер",
    "it-менеджер",
    "программист 1С",
    "web-дизайнер",
    "frontend-разработчик",
    "архитектор",
    "backend-разработчик",
    "менеджер проекта",
    "ведущий программист",
    "программист php",
    "руководитель проекта",
    "специалист по юзабилити",
    "продакт-менеджер",
    "программист mysql",
    "системный аналитик",
    "программист C#",
    "программист ЧПУ",
    "ведущий специалист",
    "технический консультант",
    "менеджер интернет-проекта",
    "инженер-программист",
    "консультант по IT",
    "главный дизайнер",
    "hr-специалист",
    "младший программист",
    "главный программист",
    "программист С++",
    "программист net",
    "ведущий аналитик",
    "разработчик баз данных",
    "специалист по внедрению erp-систем",
    "интернет-маркетолог",
    "архитектор баз данных",
    "главный аналитик",
    "инженер по автоматизации",
    "программист 3D-графики",
    "программист микроконтроллеров",
    "консультант по управлению",
    "менеджер по развитию",
    "it-администратор",
    "программист javascript",
    "программист Битрикс",
    "системный администратор",
    "специалист по управленческому учету",
    "программист мобильных приложений",
]


class Specialization(BaseModel):
    id: int
    label: str


class Industry(BaseModel):
    id: int
    name: str


class Catalog(BaseModel):
    specializations: list[Specialization]
    industries: list[Industry]


def get_catalog() -> Catalog:
    with open(CATALOG_PATH) as file:
        return Catalog(**json.load(file))


def get_it_spec_ids() -> list[int]:
    catalog = get_catalog()
    result: list[int] = []
    for spec in catalog.specializations:
        if spec.label in IT_SPECIALIZATIONS:
            result.append(spec.id)
    return result