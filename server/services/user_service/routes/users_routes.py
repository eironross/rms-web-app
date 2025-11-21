from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from schemas.user_schema import UserResponse, User, UserUpdate, UserID
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_crud import update_user, delete_user, get_user, get_all_users
from core.db.session import get_db, engine
from sqlalchemy import text, select
import httpx

routers = APIRouter(prefix="/users") 

AUTH_SERVICE_VALIDATE_URL = "http://auth_service:8000/auth/users/me"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlaXJvbi5mbG9yZXNAZm9udGFpbmUuY29tIiwiZXhwIjoxNzYzNjQxNjI0fQ.R0JSS3EME9ibl4er-wCxY3ZHDJ_hbivjxKr8ywFjQbU"


db_dependency = Annotated[AsyncSession, Depends(get_db)]

@routers.get("/health", status_code=status.HTTP_200_OK)
async def health():
    try:    
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "api": "user  route"}
    except Exception:
        return {"status": "error", "database": "user_service"}
    
@routers.get("/get-user/{id}", status_code=status.HTTP_200_OK)
async def get_user_route(id: int, db: db_dependency):
    
    user = await get_user(id, db)
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When retriving the user."
        )
        
    return UserResponse(
        user=user, 
        message="Successfully retrieve the user",
        status=200
    )
@routers.get("/get-all/", status_code=status.HTTP_200_OK)
async def get_users_routes(
    db: db_dependency,
    page: int = Query(1, ge=1),  
    size: int = Query(10, ge=1, le=100)
):
    ## apply paginate
    user = await get_all_users(db, page, size)
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When retriving the user."
        )
        
    return UserResponse(
        user=user, 
        message="Successfully retrieve the user",
        status=200
    )
    
@routers.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_users_route(id: int, payload: UserUpdate, db: db_dependency):
    
    user = await update_user(id, payload, db)
    
    if not user:
        raise HTTPException(
            status_code=200,
            detail="Something went wrong. When updating the user."
        )
    
    return UserResponse(
        user=user,
        message=f"Updated the user {id}",
        status=201
        
    )

@routers.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_users_route(id: int, db: db_dependency):

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
    