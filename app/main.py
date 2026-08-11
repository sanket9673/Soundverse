from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import setup_logging

# Import models to ensure they are registered with Base metadata
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables are created on startup
    Base.metadata.create_all(bind=engine)
    yield


setup_logging()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/health", status_code=200)
def health_check() -> dict:
    return {"status": "ok", "environment": settings.ENV}