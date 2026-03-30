from pydantic import EmailStr, BaseModel, Field
from typing import Optional, Union, List
from datetime import datetime
from core.config import settings

import uuid

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

class UserLoggedIn(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: EmailStr | None = None    

# API Reponses
class MetaData(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = settings.APP_VERSION
    database: str = "auth_services"
    pagination: Optional[List] = None


class UserResponse(BaseModel):
    data: Union[TokenData, UserOut]
    tokens: Optional[Token] = None
    metadata: MetaData = Field(default_factory=MetaData)
    message: str = "New user created"
    success: bool = True

    class Config:
        from_attributes = True
        
# Service Response

class HomeResponse(BaseModel):
    message: str
    status: str = "ok"
    service: str = "auth_services"
    database: str = "rms_db"
    