from sqlalchemy.exc import SQLAlchemyError
from .session import engine
from .base_class import Base
from models.auth_model import UserJunctionModel, UserModel, UserProfileModel, UserRoleModel

async def create_db_and_tables() -> None:
    async with engine.begin() as async_connection:
        try: 
            await async_connection.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as exc:
            print("Error creating tables:", exc)
            
