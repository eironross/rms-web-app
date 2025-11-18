import asyncio

from typing import Optional, Any, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
        AsyncEngine, AsyncSession, create_async_engine, AsyncTransaction
)
from .session import engine, get_db
from .base_class import Base
from sqlalchemy import select

async def create_db_and_tables():
    async with engine.begin() as async_connection:
        try: 
            await async_connection.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as exc:
            print("Error creating tables:", exc)
            


        