## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

## Service Import
from models.auth_model import UserModel

## Common
from core.auth.password import AuthService

auth = AuthService()

async def authenticate_users(
    payload: OAuth2PasswordRequestForm,
    session: AsyncSession
):
    async with session as db:
        try:
            result = (await db.execute(
                select(UserModel).where(UserModel.email == payload.username)
            )).scalar_one_or_none()
            
            print(result)
            
            if not result:
                return False
            if not await auth.check_password(payload.password, hashed_password=result.hashed_password):
                return False
            
            return result
            
        except Exception as e: 
            print(f"Error occured in {e}")
            raise
           

