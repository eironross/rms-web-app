from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from schemas.user_schema import UserResponse, User, UserUpdate, UserID, HomeResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_crud import update_user, delete_user, get_user, get_all_users
from core.db.session import get_db, engine
from sqlalchemy import text, select
import httpx

routers = APIRouter(prefix="/users") 

AUTH_SERVICE_VALIDATE_URL = "http://auth_service:8000/auth/users/me"

db_dependency = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user_from_auth_service(request: Request):
    """
    Call the Auth Service to validate the user via token.
    The token can come from Authorization header or HttpOnly cookie.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    access_token = request.cookies.get("access_token")
    
    if access_token is None:
        raise credentials_exception
    print(request.cookies)
    
    headers = {"Authorization": f"{access_token}"}
    print(headers)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(AUTH_SERVICE_VALIDATE_URL, headers=headers)
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cannot reach Auth Service"
            )

    if response.status_code != 202:
        raise credentials_exception

    return response.status_code  # This is the user data

@routers.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
async def health():
    """ Determine if the route up and running"""
    try:    
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return HomeResponse(
        message="Welcome to my User Services, home route /auth/health",
        )
    except Exception:
        return HomeResponse(
            message="Error occured in the system",
            status="error"
        )
    
@routers.get("/get-user/{id}", status_code=status.HTTP_200_OK)
async def get_user_route(id: int, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """Get a one user from the user db"""
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
    auth: Annotated[int, Depends(get_current_user_from_auth_service)],
    page: int = Query(1, ge=1),  
    size: int = Query(10, ge=1, le=100)
):
    """Get a all users from the user db while also paginating the users based of the request"""
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
async def update_users_route(id: int, payload: UserUpdate, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """Updates the user information in the db"""
    
    if auth != 202:
        raise HTTPException(
            status_code=200,
            detail="Something went wrong, its you not me.... :("
        )
    
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
async def delete_users_route(id: int, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """ Deletes one user from the user db"""
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
    