from fastapi import FastAPI, status
from sqlalchemy import text
from contextlib import asynccontextmanager

## Common Imports
from core.db.db_init import create_db_and_tables
from core.db.session import engine
from routes import __routers__
from schemas.user_schema import HomeResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_db_and_tables()
    except Exception as e:
        print("Lifespan startup failed:", e)
        raise
    yield
    
app = FastAPI(lifespan=lifespan)

for route in __routers__:
    app.include_router(route)

@app.get("/", status_code=status.HTTP_200_OK, response_model=HomeResponse)
async def root():
    return HomeResponse(
        message="Welcome to my Auth Services",
        )
    
@app.get("/health", tags=["health"], status_code=status.HTTP_200_OK, response_model=HomeResponse)
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return HomeResponse(
        message="Welcome to my Auth Services",
        )
    except Exception:
        return HomeResponse(
            message="Error occured in the system",
            status="error"
        )