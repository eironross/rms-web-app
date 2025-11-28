from fastapi import FastAPI, status
from sqlalchemy import text
from schemas.auth_schema import HomeResponse

## Common Imports
from db.session import engine
from routes import __routers__
from core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

for route in __routers__:
    app.include_router(route, prefix="/api/v1")

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
            message="Status ok connected to a database"
        )
    except Exception:
        return HomeResponse(
            message="Error occured in the system",
            status="error"
        )