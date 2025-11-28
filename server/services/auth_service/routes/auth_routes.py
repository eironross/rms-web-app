from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta

from schemas.auth_schema import (
    TokenData, 
    UserResponse, 
    UserOut, 
    User)
from core.password import AuthService
from db.session import get_db
from crud.auth_crud import (
    authenticate_users, 
    get_user, 
    create_user
    )
from core.config import settings
from core.logger import get_logger

# Instance of the logger
logger = get_logger(__name__)

# Instance of the router path
routers = APIRouter(prefix="/auth") 

# Instance of the Auth Service Class
auth = AuthService()

# Route for acquiring tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency on the database sessions
db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def token_from_request(request: Request):
    # Try Authorization header first
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]

    # Fallback: HttpOnly cookie
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        # If you stored it as "Bearer <token>", remove "Bearer "
        if cookie_token.startswith("Bearer "):
            return cookie_token.split(" ")[1]
        return cookie_token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token missing"
    )

# verify the user from the db
async def get_current_user(
    db: db_dependency,
    request: Request)-> UserOut:
    """Verifies the user token and the user email if valid"""
    
    logger.info("Verifiying user and token, Just wait a little..")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info("Checking the access tokens")
    access_token = await token_from_request(request)
    logger.error(f"No token received {access_token}")
    
    try:
        logger.info("Decoding the access tokens")
        payload = await auth.decode_access_token(token=access_token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        logger.error("Token aren't valida")
        raise credentials_exception
    
    logger.info("Tokens are validated, Checking the user in the database")
    user = await get_user(username, db)
    if user is None:
        logger.error("User not found, token might maliciously")
        raise credentials_exception
    logger.info("User verified returning response!")
    return user
    
@routers.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login_for_access_tokens(
    response: Response, 
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):  
    """Generates the token for the logged in users in the systems"""
    
    logger.info("Logging User..")
    users = await authenticate_users(payload, db)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth.create_access_token(
        payload={
            "sub": users.email
            },
        expires_delta=access_token_expires
        )
    logger.info("Setting the cookie for the browser")
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,  # set TRUE in production (requires HTTPS)
        samesite="lax",
        max_age=360000,
        path="/",
    )
    
    logger.info("User logged in, good luck out there!")
    return {
        "message": "User logged in",
        "cookie": response
    }
    
@routers.post("/logout")
def logout(response: Response):
    logger.info("User logged out!")
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@routers.get("/users/me", status_code=status.HTTP_202_ACCEPTED)
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):  
    logger.info("/user/me was called, verifiying the tokens")
    return UserResponse(
        data=TokenData(
            email=current_user.email
        ),
        message="Hello World from the another world!"
    )
    
@routers.post("/register", status_code=status.HTTP_200_OK)
async def create_users_route(payload: User, db: db_dependency):
    
    logger.info("Registering the user, will get back!")
    user = await create_user(payload, db)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. When creating the user. User may already be registered.."
        )
    
    logger.info("User registered. Returning a response to the client")    
    return UserResponse(
        data=user, 
        message="Successfully created new user",
        status=201
    )