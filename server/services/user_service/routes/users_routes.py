from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from schemas.user_schema import UserResponse, User, UserUpdate, UserID
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_crud import create_user, update_user, delete_user, get_user, get_all_users
from core.db.session import get_db, engine
from sqlalchemy import text, select
import httpx

routers = APIRouter(prefix="/users") 

AUTH_SERVICE_VALIDATE_URL = "http://auth_service:8000/auth/users/me"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlaXJvbi5mbG9yZXNAZm9udGFpbmUuY29tIiwiZXhwIjoxNzYzNjQxNjI0fQ.R0JSS3EME9ibl4er-wCxY3ZHDJ_hbivjxKr8ywFjQbU"

async def check_auth() -> bool:
    
    try:
        async with httpx.AsyncClient() as client:
            print("Sending request to auth service")
            response = await client.get(
                url=AUTH_SERVICE_VALIDATE_URL,
                headers={"Authorization": f"Bearer {TOKEN}"},
                timeout=5.0
            )
            response.raise_for_status()
            
            data = response.json()
            
            return data.get("success", False)
    
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is unavailable",
    )


auth = Annotated[bool, Depends(check_auth)]
db_dependency = Annotated[AsyncSession, Depends(get_db)]

@routers.get("/health", status_code=status.HTTP_200_OK)
async def health(is_auth: auth):
    try:
        print(is_auth)
        if not is_auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token validation failed. User is not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
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
    is_auth: auth,
    page: int = Query(1, ge=1),  
    size: int = Query(10, ge=1, le=100)
    
):
    if not is_auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token validation failed. User is not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    
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

@routers.post("/create", status_code=status.HTTP_201_CREATED)
async def create_users_route(payload: User, db: db_dependency):
   
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
    
@routers.put("/update/{id}", status_code=status.HTTP_201_CREATED)
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

@routers.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
    