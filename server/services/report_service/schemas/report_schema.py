from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from datetime import datetime
        
class HomeResponse(BaseModel):
    message: str
    status: str = "ok"
    service: str = "report_services"
    database: str = "rms_db"