from fastapi import FastAPI
from db.db_init import create_db_and_tables
from db.session import engine
from sqlalchemy import text
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_db_and_tables()
    except Exception as e:
        print("Lifespan startup failed:", e)
        raise
    yield

app = FastAPI(lifespan=lifespan)

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