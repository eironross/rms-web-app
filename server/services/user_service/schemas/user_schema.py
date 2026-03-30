from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union, Literal
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
    

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[List[str]] = None

class UserID(BaseModel):
    id: int
    response_type: Literal["id_only"] = "id_only"

class UserOut(UserBase):
    id: Optional[int] = None
    email: EmailStr
    role: List[str]
    response_type: Literal["full_report"] = "full"
        
    class Config:
        from_attributes = True
    
class UserAll(BaseModel):
    total_count: int
    page: int
    size: int
    users: List[UserOut]
    response_type: Literal["all"] = "all"
    
# API Reponses

class MetaData(BaseModel):
    request_id: int = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = settings.APP_VERSION
    database: str = "user_services"
    pagination: Optional[List] = None

class UserResponse(BaseModel):
    data: Optional[Union[UserOut, UserID, UserAll]] = Field(None, discriminator="response_type")
    metadata: MetaData = Field(default_factory=MetaData)
    message: str = "New user created"
    success: bool = True
   
    class Config:
        from_attributes = True
        
class HomeResponse(BaseModel):
    message: str
    status: str = "ok"
    service: str = "user_services"
    database: str = "rms_db"