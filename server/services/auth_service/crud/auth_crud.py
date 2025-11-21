## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from pydantic import EmailStr

## Service Import
from models.auth_model import UserModel, UserRoleModel, UserProfileModel
from schemas.auth_schema import UserOut, User

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
           
async def create_user(payload: User, session: AsyncSession) -> UserOut:
    async with session as db:
        try: 
            ## fetch data from the roles table
            
            user = (await db.execute(
                select(UserModel).where(UserModel.email == payload.email)
            )).scalar_one_or_none()
            
            if user:
                raise HTTPException(
                    status_code=400,
                    detail="User already registered!"
                )
            
            result = (await db.execute(
                select(UserRoleModel).where(UserRoleModel.role.in_(payload.role))
            )).scalars().all()
            
            hashed_password = await auth.hash_password(payload.password)
            
            new_user = UserModel(
                hashed_password=hashed_password,
                email=payload.email, 
                profile=UserProfileModel(
                    first_name=payload.first_name,
                    last_name=payload.last_name
                ),
                roles=result
            )
            
            db.add(new_user) 
            await db.commit()
            await db.refresh(new_user)
            
            return UserOut(
                first_name=new_user.profile.first_name,
                last_name=new_user.profile.last_name,
                email=new_user.email,
                role=[r.role for r in new_user.roles]
            )
        except Exception as e: 
            print(f"Error occured in {e}")
            raise
