from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user_model import UserModel, UserProfileModel, UserRoleModel
from schemas.user_schema import User, UserOut
from auth.password import hash_password
from db.session import get_db
## http exception handler


async def create_user(payload: User, session: AsyncSession) -> UserOut:
        try: 
            ## fetch data from the roles table
            result = (await session.execute(
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
            
            session.add(new_user) 
            await session.commit()
            await session.refresh(new_user)
            
            return UserOut(
                first_name=new_user.profile.first_name,
                last_name=new_user.profile.last_name,
                email=new_user.email,
                role=[r.role for r in new_user.roles]
            )
        except Exception as e: 
            print(f"Error occured in {e}")
            raise