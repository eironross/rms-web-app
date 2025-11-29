from sqlalchemy import text
import httpx

from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from crud.user_crud import update_user, delete_user, get_user, get_all_users
from db.session import get_db, engine
from schemas.user_schema import UserResponse, UserUpdate, UserID, HomeResponse
from core.logger import get_logger

logger = get_logger(__name__)

# Routes for the Users
routers = APIRouter(prefix="/users") 

# Database dependency for Depends
db_dependency = Annotated[AsyncSession, Depends(get_db)]

# Validate tokens received from the cookies
async def get_current_user_from_auth_service(request: Request):
    """
    Call the Auth Service to validate the user via token.
    The token can come from Authorization header or HttpOnly cookie.
    """
    logger.info("Validating the user to the Auth Services")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    ## add header validation
    logger.info(request.headers)
    ## cookie tokens
    access_token = request.cookies.get("access_token")
    bearer_token = {"Authorization": f"{access_token}"}
    logger.info(headers)
    
    headers = request.headers if access_token is None else bearer_token
    async with httpx.AsyncClient() as client:
        try:    
            logger.info(f"Calling the Auth Serivices, {settings.AUTH_SERVICE_URL}")
            response = await client.get(settings.AUTH_SERVICE_URL, headers=headers)
            logger.info("The remote server return their reponse..")
        except httpx.RequestError:
            logger.error("Error occured: Service may not be available")
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
        logger.info("Just checking your health.")
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Aight you good.~")    
        return HomeResponse(
        message="Welcome to my User Services, home route /auth/health",
        )
    except Exception:
        logger.error("Whoops, not good!")
        return HomeResponse(
            message="Error occured in the system",
            status="error"
        )
    
@routers.get("/get-user/{id}", status_code=status.HTTP_200_OK)
async def get_user_route(id: int, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """Get a one user from the user db"""
    
    logger.info("/get-user/ was called, Getting a user from the db")
    user = await get_user(id, db)
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When retriving the user."
        )
    logger.info("Returning a response")
    return UserResponse(
        data=user, 
        message="Successfully retrieve the user",
        status=200
    )
@routers.get("/get-all", status_code=status.HTTP_200_OK)
async def get_users_routes(
    db: db_dependency,
    auth: Annotated[int, Depends(get_current_user_from_auth_service)],
    page: int = Query(1, ge=1),  
    size: int = Query(10, ge=1, le=100)
):
    """Get a all users from the user db while also paginating the users based of the request"""
    ## apply paginate
    logger.info("/get-all/ was called, Getting a user from the db")
    user = await get_all_users(db, page, size)
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When retriving the user."
        )
    logger.info("The task was successful returning a response.")
    return UserResponse(
        data=user, 
        message="Successfully retrieve the user",
        status=200
    )
    
@routers.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_users_route(id: int, payload: UserUpdate, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """Updates the user information in the db"""
    logger.info("/update/ was called, Updating a user in the db")

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
    logger.info("The task was successful returning a response.")
    return UserResponse(
        data=user,
        message=f"Updated the user {id}",
        status=201
        
    )

@routers.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_users_route(id: int, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """ Deletes one user from the user db"""
    logger.info("/deleting/ was called, deleting a user in the db. Reminder make sure that this is not your own id")
    # add validator if the id equal to the id of the current_user, cant delete the user while in active session
    
    user = await delete_user(id, db)
    
    print(f"Deleted user {user}")
    
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When deleting the user."
        )
    logger.info("The task was successful returning a response.")
    return UserResponse(
        data=UserID(id=id),
        message=f"Sucessfully deleted the user, {id}",
        status=204
    )
    