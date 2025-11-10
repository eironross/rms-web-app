from typing import Optional, Any, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
        AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
)
from .config import create_url

DATABASE_URI = create_url()


print(DATABASE_URI)

engine: AsyncEngine = create_async_engine(url=DATABASE_URI, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
  async with AsyncSessionLocal() as session:
    try:
        yield session
    except SQLAlchemyError as exc:
        await session.rollback()
        raise exc


async def get_session() -> AsyncSession:
    session: Optional[AsyncSession] = None
    async for session in get_db():
        break
    if session is None:
        raise RuntimeError("No database session available!")
    return session