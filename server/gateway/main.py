from fastapi import FastAPI, HTTPException, status, Depends, Request, Cookie
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
import httpx
import os

SERVICE_DISCOVERY = {
    "auth_service": os.environ.get("AUTH_SERVICE_URL"),
    "user_service": os.environ.get("USER_SERVICE_URL")   
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
       i for i in SERVICE_DISCOVERY.values()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the API gateway for the Reporting Services"
        }
    
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def dynamic_routing(full_path: str, request: Request, access_token: str = Cookie(None)):
    """ Dynamic Route to access any method then forward the request to appropriate services"""
    ## String Manipulate to create a target service url for the client
    target_service_url = None
    stripped_path = None
    for prefix, service_url in SERVICE_DISCOVERY.items():
        if full_path.startswith(prefix):
            target_service_url = service_url
            stripped_path = full_path[len(prefix):] or "/"
            print(full_path)
            break
    if target_service_url is None:
        raise HTTPException(status_code=404, detail="Service not found")

    # Construct full target URL
    target_url = f"{target_service_url}{stripped_path}"
    print(f"Final generated path: Full Path: {full_path} Target Full URL: {target_url} Target Service: {target_service_url} Stripped: {stripped_path}")
    try:
    # Forward the request, including method, headers, query params, and body
        async with httpx.AsyncClient() as client:
            backend_response = await client.request(
                method=request.method,
                url=target_url,
                headers=dict(request.headers),
                params=request.query_params,
                content=await request.body(),
                timeout=10.0
            )
            
            response = Response(
                content=backend_response.content,
                status_code=backend_response.status_code,
                headers=dict(backend_response.headers)
            )
            
            return response
           
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
