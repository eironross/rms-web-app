from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    job_title: str
    facility: Optional[str] = None
    
    

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    job_title: str
    facility: Optional[str] = None
    

    class Config:
        orm_mode = True  # allows returning SQLAlchemy models directly