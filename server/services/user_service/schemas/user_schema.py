from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from datetime import datetime

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

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[List[str]] = None
    
class UserID(BaseModel):
    id: int
    
class UserAll(BaseModel):
    total_count: int
    page: int
    size: int
    users: List[UserOut]

class UserResponse(BaseModel):
    user: Optional[Union[UserOut, UserID, UserAll]] = None
    message: str = "New user created"
    status: int = 200
    database: str = "user_service"
    return_in: datetime = datetime.now()
    success: bool = True

    class Config:
        from_attributes = True
        
class HomeResponse(BaseModel):
    message: str
    status: str = "ok"
    service: str = "user_services"
    database: str = "rms_db"