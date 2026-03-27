from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from datetime import datetime
        
        
# Create inputs for the report

        
        
class HomeResponse(BaseModel):
    message: str
    status: str = "ok"
    service: str = "report_services"
    database: str = "rms_db"