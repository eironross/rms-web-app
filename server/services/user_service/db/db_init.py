import asyncio

from typing import Optional, Any, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
        AsyncEngine, AsyncSession, create_async_engine, AsyncTransaction
)
from .session import engine, get_db
from .base_class import Base
from models.user_model import UserRoleModel
from sqlalchemy import select

async def create_db_and_tables():
    async with engine.begin() as async_connection:
        try: 
            await async_connection.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as exc:
            print("Error creating tables:", exc)
            
async def create_dim_tables():
    async with get_db() as db:
        user_roles_data = {
            1: "admin",
            2: "regulatory",
            3: "trader"
            }
        
        print(f"Inside the create dim: {db}")
        try: 
            is_exists = (await db.execute(select(UserRoleModel))).scalars().first()
            if is_exists:
                
                return
            
            roles = [UserRoleModel(id=key, role=value) for key, value in user_roles_data.items()]
            db.add_all(roles)
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(f"Error occured: {e}" )

        