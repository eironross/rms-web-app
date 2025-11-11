from fastapi import APIRouter, HTTPException, Depends
from schemas.user_schema import UserResponse, UserOut, User, RoleReponse
from models.user_model import UserModel, UserRoleModel
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_crud import create_user
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
async def create_users_route(payload: User):
    async with get_db() as session:
        new_users = await create_user(payload, session)

        if not new_users:
            raise HTTPException(
                status_code=400,
                detail="Something went wrong. When creating the user."
            )
    return UserResponse(
        user=new_users
    )

@routers.get("/test")
async def get_roles_route():
    async with get_db() as db:
        print(f"In the route itself {db}")
        result = (await db.execute(
                select(UserRoleModel))
            ).scalars().all()
        roles = [r.role for r in result]
    return RoleReponse(role=roles)