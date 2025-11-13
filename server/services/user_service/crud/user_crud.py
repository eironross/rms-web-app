from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.user_model import UserModel, UserProfileModel, UserRoleModel
from schemas.user_schema import User, UserOut, UserID
from auth.password import hash_password
from fastapi import HTTPException
## http exception handler


async def create_user(payload: User, session: AsyncSession) -> UserOut:
    async with session as db:
        try: 
            ## fetch data from the roles table
            result = (await db.execute(
                select(UserRoleModel).where(UserRoleModel.role.in_(payload.role))
            )).scalars().all()
            
            new_user = UserModel(
                hashed_password=hash_password(payload.password),
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

async def update_user(id: int, payload: UserID, session: AsyncSession) -> UserOut:
    async with session as db:
        try:
            
            result = (await db.execute(
                select(UserModel).where(UserModel.id == id)
            )).scalar_one_or_none()
            
            print(result)
            
            if not result:
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
                email=result.email,
                role=[r.role for r in result.roles] if result.roles else None
            )
            
        except Exception as e:
            print(f"Error occured in {e}")
            raise