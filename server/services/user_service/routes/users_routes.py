from fastapi import APIRouter, HTTPException, Depends
from schemas.user_schema import UserResponse, User, UserID
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_crud import create_user, update_user
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

@routers.post("/create")
async def create_users_route(payload: User, db: Annotated[AsyncSession, Depends(get_db)]):
   
    user = await create_user(payload, db)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When creating the user."
        )
    return UserResponse(
        user=user
    )
    
@routers.put("/update/{id}")
async def update_users_route(id: int, payload: UserID, db: Annotated[AsyncSession, Depends(get_db)]):
    
    user = await update_user(id, payload, db)
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When creating the user."
        )
    
    return UserResponse(
        user=user
    )