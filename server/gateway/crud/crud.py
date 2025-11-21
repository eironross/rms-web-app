
import os
from fastapi import HTTPException, status, Depends
import httpx
from typing import Annotated


TOKEN=""

async def check_auth() -> bool:
    
    try:
        async with httpx.AsyncClient() as client:
            print("Sending request to auth service")
            response = await client.get(
                url=os.environ.get("AUTH_SERVICE_URL"),
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
def auth():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token validation failed. User is not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


auth = Annotated[bool, Depends(check_auth)]