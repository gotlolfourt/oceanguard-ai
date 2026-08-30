import logging
import time
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.errors import AppError, app_error_handler, generic_error_handler
from app.core.logging import configure_logging
from app.database import Base, SessionLocal, engine
from app.services.seed import seed_database

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="OceanGuard AI API", description="Marine Debris Detection Platform API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_rate_buckets: dict[str, deque[float]] = defaultdict(deque)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("request path=%s method=%s status=%s elapsed_ms=%.2f", request.url.path, request.method, response.status_code, elapsed_ms)
    return response


@app.middleware("http")
async def simple_rate_limit(request: Request, call_next):
    identifier = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = _rate_buckets[identifier]

    while bucket and bucket[0] <= now - settings.RATE_LIMIT_WINDOW_SECONDS:
        bucket.popleft()

    if len(bucket) >= settings.RATE_LIMIT_REQUESTS:
        return JSONResponse(status_code=429, content={"error": "Too many requests", "status": 429, "details": {"window_seconds": settings.RATE_LIMIT_WINDOW_SECONDS}})

    bucket.append(now)
    return await call_next(request)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get("/health")
async def health_check():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    finally:
        db.close()
    return {"status": "healthy", "service": "backend"}


@app.get("/")
async def root():
    return {"message": "OceanGuard AI API v0.1.0"}


app.include_router(api_router)
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, generic_error_handler)
