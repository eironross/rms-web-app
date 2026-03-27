## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from pydantic import EmailStr

## Service Import
from models.report_model import ReportModel, StatusModel, EventTypeModel, UnitNoModel
from schemas.report_schema import HomeResponse

# create auth ng user, track yung id or session, paratmeter to the create_report

async def create_user(payload: User, db: AsyncSession) -> UserOut:
    try: 
        ## fetch data from the roles table
        print("Test")
        user = (await db.execute(
            select(UserModel).where(UserModel.email == payload.email)
        )).scalar_one_or_none()
        print(user)
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
