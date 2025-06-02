"""Entry point for vacancy-aggregator-backend application."""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """Test endpoint."""
    return {"message": "Hello World!"}
