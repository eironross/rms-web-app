## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import List

## Service Import
from models.user_model import UserModel, UserProfileModel, UserRoleModel
from schemas.user_schema import User, UserOut, UserID, UserUpdate, UserAll



async def get_user(id: int, session: AsyncSession) -> UserOut:
    async with session as db:
        try:
            result = (await db.execute(
                select(UserModel).where(UserModel.id == id)
            )).scalar_one_or_none()
            
            if result is None:
                raise HTTPException(status_code=404, detail="User can't be found.")
            
            return UserOut(
                id=result.id,
                first_name=result.profile.first_name,
                last_name=result.profile.last_name,
                email=result.email,
                role=[r.role for r in result.roles]
            )
            
        except Exception as e: 
            print(f"Error occured in {e}")
            raise
        
async def get_all_users(session: AsyncSession, page: int = 1, size: int = 10)-> UserAll:
    
    async with session as db:
        try:
            offset = (page - 1) * size
            total_count = (await db.execute(
                select(func.count(UserModel.id))
            )).scalar()
            
            result = (await db.execute(
                select(UserModel)
                .options(
                    selectinload(UserModel.roles),
                    selectinload(UserModel.profile)
                )
                .offset(offset).limit(size)
            )).scalars().all()
            print(result)
            print(len(result))
            
            users = [UserOut.model_validate({
                "id": u.id,
                "first_name": u.profile.first_name,
                "last_name": u.profile.last_name,
                "email": u.email,
                "role": [r.role for r in u.roles]
            })
                for u in result]
            
            print(users)
            return UserAll(
                total_count=total_count, 
                page=page,
                size=size,
                users=users
            )
            
        except Exception as e:
            print(f"Error occured in {e}")
            raise 

async def update_user(id: int, payload: UserUpdate, session: AsyncSession) -> UserOut:
    async with session as db:
        try:
            
            result = (await db.execute(
                select(UserModel).where(UserModel.id == id)
            )).scalar_one_or_none()
            
            print(result)
            
            if result is None:
                raise HTTPException(status_code=404, detail="User can't be found.")
            

            for key, value in payload.model_dump(exclude_unset=True, exclude={"first_name", "last_name", "role"}).items():
                setattr(result, key, value)
            
            ## Update the UserModel
            if not result.profile:
                result.profile = UserProfileModel()
            if payload.first_name:
                result.profile.first_name = payload.first_name
            if payload.last_name:
                result.profile.last_name = payload.last_name
            
            if payload.role:
                result.roles.clear()  # remove old associations, removes links to the user_xref 

                # call again the UserRole table
                role_list = (await db.execute(
                    select(UserRoleModel).where(UserRoleModel.role.in_(payload.role))
                )).scalars().all()
                
                # append the list and update the xref
                result.roles.extend(role_list) 
                            
            await db.commit()
            await db.refresh(result)
            
            return UserOut(
                first_name=result.profile.first_name if result.profile else None,
                last_name=result.profile.last_name if result.profile else None,
                email=result.email if result.email else None,
                role=[r.role for r in result.roles] if result.roles else None
            )
            
        except Exception as e:
            print(f"Error occured in {e}")
            raise
        

async def delete_user(id: UserID, session: AsyncSession) -> UserID:
    async with session as db:
        try:
            result = (await db.execute(
                select(UserModel).where(UserModel.id == id)
            )).scalar_one_or_none()
            
            print(f"Return the user to {result}")
            
            if result is None:
                raise HTTPException(status_code=404, detail="User can't be found.")
            
            await db.delete(result)
            await db.commit()
            
            return result
         
        except Exception as e:
            print(f"Error occured in {e}")
            raise