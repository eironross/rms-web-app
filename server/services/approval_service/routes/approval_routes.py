from sqlalchemy import text
import httpx

from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from crud.approval_crud import submit_report
from db.session import get_db, engine

from schemas.approval_schema import (
    ApprovalBase
    ,ApprovalAll
    ,ApprovalID
    ,ApprovalOut
    ,ApprovalReponse
    ,ApprovalUpdate
    ,MetaData
    ,ApprovalReponse
    ,HomeResponse
)

from core.logger import get_logger

logger = get_logger(__name__)

# Routes for the Users
routers = APIRouter(prefix="/approval") 

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
    
    headers = request.headers if access_token is None else bearer_token
    logger.info(headers)
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
        message="Welcome to my Approval Services, home route /approval/health",
        )
    except Exception:
        logger.error("Whoops, not good!")
        return HomeResponse(
            message="Error occured in the system",
            status="error"
        )
        
@routers.post("/submit", status_code=status.HTTP_200_OK)
async def submit_report_route(payload: ApprovalBase, db: db_dependency) -> ApprovalReponse:
    
    logger.info("Submitting the report, will get back!")
    result = await submit_report(payload, db)
    
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When creating the report. Report may already be registered.."
        )
    
    logger.info("Successfully created new request for Approval. Returning a response to the client")    
    return ApprovalReponse(
        data=result, 
        message="Successfully created new request for Approval"
    )
        
