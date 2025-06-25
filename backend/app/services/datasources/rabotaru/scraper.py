"""
Traverse Rabota.ru, download vacancies, and save them as JSON.

Usage examples:
    python -m app.services.datasources.rabotaru.scraper # default 100 vacancies -> vacancies.json

    python -m app.services.datasources.rabotaru.scraper --limit 500 \
                                                        --output data/rabota_2025-06-25.json \
                                                        --concurrency 20
"""

import argparse
import asyncio
import json
from pathlib import Path
from typing import List

from app.services.datasources.rabotaru.traverser import (
    traverse,
    VacancyShortWithUrl,
)
from app.services.datasources.rabotaru.parser import parse_vacancy
from app.api.v1.models import Vacancy


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
async def _fetch_full(
    short: VacancyShortWithUrl,
    sem: asyncio.Semaphore,
) -> Vacancy | None:
    """Wrap `parse_vacancy` with a semaphore so we don’t hammer the site."""
    async with sem:
        try:
            return await parse_vacancy(short)
        except Exception as exc:  # noqa: BLE001
            # You may want structured logging here
            print(f"[WARN] Failed to parse vacancy {short.id}: {exc}")
            return None


async def collect_vacancies(
    *,
    limit: int,
    concurrency: int,
) -> List[Vacancy]:
    """Run the whole pipeline: traverse → fetch full vacancy pages → collect."""
    print(f"Traversing Rabota.ru for up to {limit} vacancies …")
    previews: List[VacancyShortWithUrl] = await traverse(limit=limit)
    print(f"Found {len(previews)} previews, downloading full pages …")

    sem = asyncio.Semaphore(concurrency)
    tasks = [_fetch_full(short, sem) for short in previews]
    results = await asyncio.gather(*tasks)

    # Filter out any failed / None results
    vacancies = [v for v in results if v is not None]
    print(f"Successfully parsed {len(vacancies)} vacancies.")
    return vacancies


def save_as_json(vacancies: List[Vacancy], outfile: Path) -> None:
    """Serialise Pydantic models and write pretty-printed JSON."""
    data = [v.model_dump() for v in vacancies]  # `.dict()` if using Pydantic v1
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Wrote {len(vacancies)} vacancies → {outfile.resolve()}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export vacancies from Rabota.ru")
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of vacancies to fetch (default: 100)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("vacancies.json"),
        help="Path to the output JSON file (default: vacancies.json)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Number of concurrent requests when fetching full vacancy pages "
        "(default: 10)",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    vacancies = await collect_vacancies(
        limit=args.limit,
        concurrency=args.concurrency,
    )
    save_as_json(vacancies, args.output)


if __name__ == "__main__":
    asyncio.run(main())
