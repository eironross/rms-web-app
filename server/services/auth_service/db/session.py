from typing import Optional, Any, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
        AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
)
from contextlib import asynccontextmanager
from core.config import settings

engine: AsyncEngine = create_async_engine(url=settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
      session = AsyncSessionLocal()
      try:
        print(f"Inside the get_db: {session}")
        yield session
      except Exception as e:
        print(f"Error occured: {e}" )
