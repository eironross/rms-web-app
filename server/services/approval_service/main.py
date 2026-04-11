from fastapi import FastAPI, status
from sqlalchemy import text
from contextlib import asynccontextmanager

## Common Imports
from db.db_init import create_db_and_tables
from db.session import engine
from routes import __routers__
from schemas.approval_schema import HomeResponse
from core.config import get_setting
from core.logger import get_logger

logger = get_logger(__name__)

settings = get_setting()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:   
        logger.info("Creating the tables...")
        await create_db_and_tables()
    except Exception as e:
        print("Lifespan startup failed:", e)
        raise
    yield
    
app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    version=settings.APP_VERSION
    )

for route in __routers__:
    app.include_router(route, prefix="/api/v1")

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    logger.info("Hello from the root")
    return {"message": "hello"}
    
@app.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
async def health():
    try:
        logger.info("Checking health from the root")
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1 FROM approval_service.approval_history;"))
        return {"message": "hello, health check"}
    
    except Exception:
        return {"message": "hello, error"}