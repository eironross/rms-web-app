import httpx
from fastapi import HTTPException, status
import asyncio


AUTH_SERVICE_VALIDATE_URL = "http://localhost:8001/auth/users/me"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlaXJvbi5mbG9yZXNAZm9udGFpbmUuY29tIiwiZXhwIjoxNzYzNjQxNjI0fQ.R0JSS3EME9ibl4er-wCxY3ZHDJ_hbivjxKr8ywFjQbU" 

async def check_auth() -> bool:
   
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=AUTH_SERVICE_VALIDATE_URL,
                headers={"Authorization": f"Bearer {TOKEN}"},
                timeout=5.0
            )
            response.raise_for_status()
            
            data = response.json()
            
            return data
    
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


if __name__ == "__main__":
    is_check = asyncio.run(check_auth())
    
    print(is_check)