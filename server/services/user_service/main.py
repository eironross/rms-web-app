from fastapi import FastAPI
from db.db_init import create_db_and_tables, create_dim_tables
from db.session import engine
from sqlalchemy import text
from contextlib import asynccontextmanager
from routes import __routers__

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_db_and_tables()
        
        await create_dim_tables()
    except Exception as e:
        print("Lifespan startup failed:", e)
        raise
    yield
    
app = FastAPI(lifespan=lifespan)

for route in __routers__:
    app.include_router(route)

@app.get("/")
async def root():
    return {
        "message": "Welcome to my User Services",
        "status": "ok"
    }
    
@app.get("/health", tags=["health"])
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "error", "database": "unreachable"}