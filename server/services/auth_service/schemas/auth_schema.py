from pydantic import EmailStr, BaseModel
from typing import Optional, Union
from datetime import datetime

class UserLoggedIn(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    user: UserLoggedIn
    tokens: Token
    message: str = "New user created"
    status: int = 200
    database: str = "auth_service"
    return_in: datetime = datetime.now()

    class Config:
        from_attributes = True