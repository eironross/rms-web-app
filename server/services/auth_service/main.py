from fastapi import FastAPI, status
from sqlalchemy import text

## Common Imports
from core.db.session import engine
from routes import __routers__

app = FastAPI()

for route in __routers__:
    app.include_router(route)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {
        "message": "Welcome to my Auth Services",
        "status": "ok"
    }
    
@app.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "error", "database": "unreachable"}