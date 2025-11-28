from sqlalchemy.exc import SQLAlchemyError
from .session import engine
from .base_class import Base
from core.logger import get_logger

logger = get_logger(__name__)

async def create_db_and_tables() -> None:
    async with engine.begin() as async_connection:
        try:    
            logger.info("Creating the tables in the PostGreSQL")
            await async_connection.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as exc:
            logger.error("Error creating tables:", exc)
            


        