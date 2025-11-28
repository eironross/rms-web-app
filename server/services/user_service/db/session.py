from typing import Optional, Any, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
        AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
)
from core.config import settings
from contextlib import asynccontextmanager
from core.logger import get_logger

engine: AsyncEngine = create_async_engine(url=settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

logger = get_logger(__name__)

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
      session = AsyncSessionLocal()
      try:
        logger.info(f"Inside the get_db: {session}")
        yield session
      except Exception as e:
         logger.error(f"Error occured: {e}" )
     