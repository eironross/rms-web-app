from fastapi import APIRouter, HTTPException, Depends, Query, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas.auth_schema import UserLoggedIn, Token, UserResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth.password import AuthService
from core.db.session import get_db, engine
from sqlalchemy import text, select
from crud.auth_crud import authenticate_users

routers = APIRouter(prefix="/auth") 

auth = AuthService()

db_dependency = Annotated[AsyncSession, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

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
):
    users = await authenticate_users(payload, db)

    if not users:
        raise HTTPException(
            status_code=400,
            detail="User can't be verified"
        )
    
    gen_tokens = await auth.create_access_token(users)
    
    return UserResponse(
        user=UserLoggedIn(
            email=users.email,
        ),
        tokens=Token(
            access_token=gen_tokens,
            token_type="bearer"
        ),
        message="User was verified, Giving tokens"
        
    )