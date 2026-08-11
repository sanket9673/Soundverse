from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes.play import router as play_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import setup_logging
from app.monitoring.metrics import setup_metrics

import app.models  # noqa: F401

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


setup_logging()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Setup Prometheus metrics middleware and /metrics route
setup_metrics(app)

app.include_router(play_router)


# Global Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail), "code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": f"Validation Error: {exc.errors()}",
            "code": 422,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "code": 500},
    )


@app.get("/health", status_code=200)
def health_check() -> dict:
    return {"status": "ok", "environment": settings.ENV}