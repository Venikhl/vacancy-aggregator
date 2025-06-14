# vacancy-aggregator-backend

## Dependencies
- `python 3.11`
- `uv`

## Local installation 

```bash
pip install uv

git clone https://github.com/Venikhl/vacancy-aggregator
cd vacancy-aggregator
cd backend

uv venv --python 3.11
source .venv/bin/activate
uv sync --frozen 
```

note: `uv sync` ≈ `poetry install` + `poetry lock`

## Running


```bash
uv run uvicorn app.main:app
```
## API Documentation

See OpenAPI file which is located at `backend/docs/openapi.json` or use `/docs` endpoint inside the app.
