from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ServiceReponse(BaseModel):
    data: Optional[dict] = None
    message: str = "Data received from the microservices"
    status: int = 200
    return_in: datetime = datetime.now()
    
    
    


"""
    "data": {
        ...services data
    },
    message: "Data received from the microservices,
    status: 200
    return_in: 2025-11-20TZ11:12:0:022
"""