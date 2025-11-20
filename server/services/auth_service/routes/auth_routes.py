from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError

from schemas.auth_schema import UserLoggedIn, Token, TokenData, UserResponse, UserOut
from core.auth.password import AuthService
from core.db.session import get_db, engine
from sqlalchemy import text
from crud.auth_crud import authenticate_users, get_user
from datetime import timedelta
from core.auth.password import ACCESS_TOKEN_EXPIRE_MINUTES

routers = APIRouter(prefix="/auth") 

auth = AuthService()

db_dependency = Annotated[AsyncSession, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: db_dependency)-> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print('called to verify user', token)
        payload = await auth.decode_access_token(token=token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = await get_user(username, db)
    
    if user is None:
        raise credentials_exception
    return user

@routers.get("/health", status_code=status.HTTP_200_OK)
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "api": "user  route"}
    except Exception:
        return {"status": "error", "database": "unreachable"}
    
@routers.post("/token")
async def login_for_access_tokens(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
) -> Token:
    users = await authenticate_users(payload, db)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth.create_access_token(
        payload={
            "sub": users.email
            },
        expires_delta=access_token_expires
        )
    
    tokens = Token(
            access_token=access_token,
            token_type="bearer"
        )
    print(tokens)
    user = TokenData(
            email=users.email,
        )
    print("inside the post routes")
    return tokens
    
@routers.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    return UserResponse(
        user=TokenData(
            email=current_user.email
        ),
        message="Hello World from the another world!"
    )