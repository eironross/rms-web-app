from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union, Literal
from datetime import datetime, date, time
from core.config import settings

import uuid
        
        
# Create inputs for the report
class ReportBase(BaseModel):
    title: str
    event_type_id: int
    report_details: str
    status_id: int
    unit_id: int
    event_date: date
    event_time: time

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    event_type_id: Optional[int] = None
    report_details: Optional[str] = None
    status_id: Optional[int] = None
    unit_id: Optional[int] = None
    event_date: Optional[date] = None
    event_time: Optional[time] = None

# CRUD schema     
class ReportID(BaseModel):
    id: int
    response_type: Literal["id_only"] = "id_only"
    
class ReportOut(ReportBase):
    id: Optional[int] = None
    status_name: Optional[str] = None
    unit_name: Optional[str] = None
    event_name: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime
    response_type: Literal["full_report"] = "full"
    
    class Config:
        from_attributes = True   
        
class ReportAll(BaseModel):
    total_count: int
    page: int
    size: int
    reports: List[ReportOut]
    response_type: Literal["all"] = "all"

# API Reponses

class MetaData(BaseModel):
    request_id: int = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = settings.APP_VERSION
    database: str = "report_services"
    pagination: Optional[List] = None
        
class ReportReponse(BaseModel):
    data: Optional[Union[ReportOut, ReportID, ReportAll]] = Field(None, discriminator="response_type")
    metadata: MetaData = Field(default_factory=MetaData)
    message: str = "New report created"
    success: bool = True     
    
    class Config:
        from_attributes = True
        
class HomeResponse(BaseModel):
    message: str
    status: str = "ok"
    service: str = "report_services"
    database: str = "rms_db"