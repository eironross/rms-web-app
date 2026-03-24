from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .session import engine
from .base_class import Base
from core.logger import get_logger
from models.report_model import ReportModel ## important to import the model before creating the tables


logger = get_logger(__name__)

async def create_db_and_tables() -> None:
    async with engine.begin() as async_connection:
        try:    
            logger.info("Creating the tables in the PostGreSQL")
            ##logger.info(Base.metadata.tables)
    
            logger.info(Base.metadata.tables.keys())
            
            
            logger.info(__name__)
            await async_connection.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as exc:
            logger.error("Error creating tables:", exc)
            


        