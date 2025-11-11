from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    role: List[str]
    
    
class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: List[str]
    
class RoleReponse(BaseModel):
    role: List[str]

    model_config = {
        'from_attributes': True
    }

class UserResponse(BaseModel):
    user: UserOut
    message: str = "New user created"
    status: str = "200"
    database: str = "user_service"
    return_in: datetime = datetime.now()

    model_config = {
        'from_attributes': True
    }