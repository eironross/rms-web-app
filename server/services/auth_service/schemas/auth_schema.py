from pydantic import EmailStr, BaseModel
from typing import Optional, Union, List
from datetime import datetime

class UserLoggedIn(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: EmailStr | None = None    

class UserResponse(BaseModel):
    user: TokenData
    tokens: Optional[Token] = None
    message: str = "New user created"
    status: int = 200
    database: str = "auth_service"
    return_in: datetime = datetime.now()
    success: bool = True

    class Config:
        from_attributes = True
        
class UserBase(BaseModel):
    first_name: str
    last_name: str
 
class User(UserBase):
    email: EmailStr
    password: str
    role: List[str] = None
    
class UserOut(UserBase):
    id: Optional[int] = None
    email: EmailStr
    role: List[str]
    
    class Config:
        from_attributes = True