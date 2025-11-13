from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
 
class User(UserBase):
    email: EmailStr
    password: str
    role: List[str] = None
    
class UserOut(UserBase):
    email: EmailStr
    role: List[str]
    

class UserID(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[List[str]] = None

class UserResponse(BaseModel):
    user: UserOut
    message: str = "New user created"
    status: str = "200"
    database: str = "user_service"
    return_in: datetime = datetime.now()

    model_config = {
        'from_attributes': True
    }