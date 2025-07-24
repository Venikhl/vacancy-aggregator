FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app

COPY . .

RUN uv sync --frozen

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
