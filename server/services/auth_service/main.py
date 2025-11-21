from fastapi import FastAPI, status
from sqlalchemy import text
from schemas.auth_schema import HomeResponse

## Common Imports
from core.db.session import engine
from routes import __routers__

app = FastAPI()

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
            message="Status ok connected to a database"
        )
    except Exception:
        return HomeResponse(
            message="Error occured in the system",
            status="error"
        )