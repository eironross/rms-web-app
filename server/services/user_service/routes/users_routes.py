from fastapi import APIRouter, HTTPException, Depends
from schemas.user_schema import UserResponse, User, UserUpdate, UserID
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_crud import create_user, update_user, delete_user
from db.session import get_db, engine  
from sqlalchemy import text, select

routers = APIRouter(prefix="/users") 

@routers.get("/health")
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "api": "user  route"}
    except Exception:
        return {"status": "error", "database": "unreachable"}
    
@routers.get("/get_user/{id}")
async def get_user(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@routers.get("/get-all/")
async def get_user(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    ## apply paginate
    pass

@routers.post("/create")
async def create_users_route(payload: User, db: Annotated[AsyncSession, Depends(get_db)]):
   
    user = await create_user(payload, db)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When creating the user."
        )
    return UserResponse(
        user=user, 
        message="Successfully created new user",
        status=201
    )
    
@routers.put("/update/{id}")
async def update_users_route(id: int, payload: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    
    user = await update_user(id, payload, db)
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When updating the user."
        )
    
    return UserResponse(
        user=user,
        message=f"Updated the user {id}",
        status=201
        
    )

@routers.delete("/delete/{id}")
async def delete_users_route(id: int, db: Annotated[AsyncSession, Depends(get_db)]):

    user = await delete_user(id, db)
    
    print(f"Deleted user {user}")
    
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When deleting the user."
        )
        
    return UserResponse(
        user=UserID(id=id),
        message=f"Sucessfully deleted the user, {id}",
        status=204
    )
    