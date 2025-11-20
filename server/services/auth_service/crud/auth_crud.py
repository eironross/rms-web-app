## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from pydantic import EmailStr

## Service Import
from models.auth_model import UserModel
from schemas.auth_schema import UserOut

## Common
from core.auth.password import AuthService

auth = AuthService()

async def get_user(email: EmailStr, 
                   session: AsyncSession) -> UserOut:
    async with session as db:
        try:
            result = (await db.execute(
                select(UserModel).where(UserModel.email == email)
            )).scalar_one_or_none()
            
            if result is None:
                raise HTTPException(status_code=404, detail="User can't be found.")
            
            return UserOut(
                first_name=result.profile.first_name,
                last_name=result.profile.last_name,
                email=result.email,
                role=[r.role for r in result.roles]
            )
            
        except Exception as e: 
            print(f"Error occured in {e}")
            raise
        


async def authenticate_users(
    payload: OAuth2PasswordRequestForm,
    session: AsyncSession
) -> UserOut:
    async with session as db:
        try:
            result = (await db.execute(
                select(UserModel).where(UserModel.email == payload.username)
            )).scalar_one_or_none()

            is_password = await auth.check_password(payload.password, hashed_password=result.hashed_password)
            
            if not result:
                return False
            
            if not is_password:
                return False
            
            return UserOut(
                first_name=result.profile.first_name,
                last_name=result.profile.last_name,
                email=result.email,
                role=[r.role for r in result.roles]
            )
            
        except Exception as e: 
            print(f"Error occured in {e}")
            raise
           

