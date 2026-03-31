from sqlalchemy import text
import httpx

from fastapi import APIRouter, HTTPException, Depends, Query, status, Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from crud.report_crud import update_report, delete_report, create_report, get_all_report, get_report
from db.session import get_db, engine
from schemas.report_schema import (
    ReportReponse, 
    ReportBase, 
    HomeResponse, 
    ReportID, 
    ReportAll, 
    ReportOut, 
    ReportUpdate, 
    MetaData)
from core.logger import get_logger

logger = get_logger(__name__)

# Routes for the Users
routers = APIRouter(prefix="/reports") 

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
        message="Welcome to my Reports Services, home route /reports/health",
        )
    except Exception:
        logger.error("Whoops, not good!")
        return HomeResponse(
            message="Error occured in the system",
            status="error"
        )
        
@routers.get("/get-report", status_code=status.HTTP_200_OK)
async def get_report_route(id: int, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]) -> ReportReponse:
    """Get a one report from the report db"""
    
    logger.info("/get-report/ was called, Getting a report from the db")
    result = await get_report(id, db)
    
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When retriving the user."
        )
    logger.info("Returning a response")
    return ReportReponse(
        data=result, 
        message="Successfully retrieve the report {id}"
    )
    
@routers.get("/get-all", status_code=status.HTTP_200_OK)
async def get_report_routes(
    db: db_dependency,
    auth: Annotated[int, Depends(get_current_user_from_auth_service)],
    page: int = Query(1, ge=1),  
    size: int = Query(10, ge=1, le=100)
) -> ReportReponse:
    """Get a all reports from the report db while also paginating the reports based of the request"""
    ## apply paginate
    logger.info("/get-all/ was called, Getting a user from the db")
    result = await get_all_report(db, page, size)
    
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When retriving the result."
        )
        
    logger.info("The task was successful returning a response.")
    return ReportReponse(
        data=result.reports, 
        metadata=MetaData(
            pagination= {
                "total_count": result.total_count,
                "page": result.page,
                "size": result.size, 
            }
        ),
        message="Successfully retrieve the result"
    )
    

@routers.post("/create", status_code=status.HTTP_200_OK)
async def create_report_route(payload: ReportBase, db: db_dependency) -> ReportReponse:
    
    logger.info("Creating the report, will get back!")
    result = await create_report(payload, db)
    
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When creating the report. Report may already be registered.."
        )
    
    logger.info("Report created. Returning a response to the client")    
    return ReportReponse(
        data=result, 
        message="Successfully created new report"
    )
        
@routers.put("/update", status_code=status.HTTP_200_OK)
async def update_report_route(id: int, payload: ReportUpdate, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """Updates the report information in the db"""
    logger.info("/update/ was called, Updating a report in the db")

    if auth != 202:
        raise HTTPException(
            status_code=200,
            detail="Something went wrong, its you not me.... :("
        )
    
    result = await update_report(id, payload, db)
    
    if not result:
        raise HTTPException(
            status_code=200,
            detail="Something went wrong. When updating the user."
        )
    logger.info("The task was successful returning a response.")
    
    return ReportReponse(
        data=result,
    )

@routers.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_report_route(id: int, db: db_dependency, auth: Annotated[int, Depends(get_current_user_from_auth_service)]):
    """ Deletes one user from the user db"""
    logger.info("/deleting/ was called, deleting a report in the db. Reminder make sure that this is not your own id")
    # add validator if the id equal to the id of the current_user, cant delete the user while in active session
    
    result = await delete_report(id, db)
    
    logger.info(f"Deleted result: {result}")
    
    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When deleting the report."
        )
    logger.info("The task was successful returning a response.")
    return ReportReponse(
        data=ReportID(id=id),
        message=f"Sucessfully deleted the report, {id}"
    )
    
