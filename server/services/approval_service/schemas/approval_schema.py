from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union, Literal
from datetime import datetime, date, time
from core.config import settings

import uuid
        
        
# Create inputs for the report
class ApprovalBase(BaseModel):
    report_id: int
    approval_level_id: int = 1 ## default approval to the Senior Energy Trader
    comment: str
    status_id: int = 1 ## default to new approval status
    created_by_id: int
    
class ApprovalUpdate(BaseModel):
    approval_level_id: Optional[int] = None
    comment: Optional[str] = None
    status: Optional[int] = None 
    modified_by_id: int
    
# CRUD schema     
class ApprovalID(BaseModel):
    id: int
    # response_type: Literal["id_only"] = "id_only"
    
class ApprovalOut(ApprovalBase):
    id: Optional[int] = None
    description: Optional[str] = None
    approval_level: Optional[str] = None
    rolename: Optional[str] = None 
    # response_type: Literal["full_report"] = "full_report"
    
    class Config:
        from_attributes = True   
        
class ApprovalAll(BaseModel):
    total_count: int
    page: int
    size: int
    reports: List[ApprovalOut]
    # response_type: Literal["all"] = "all"

# API Reponses
class MetaData(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = settings.APP_VERSION
    database: str = "approval_services"
    pagination: Optional[dict] = None
        
class ApprovalReponse(BaseModel):
    data: Optional[Union[ApprovalOut, ApprovalID, ApprovalAll, List[ApprovalOut]]] = None
    metadata: MetaData = Field(default_factory=MetaData)
    message: str = "A new has been submitted for approval"
    success: bool = True     
    
    class Config:
        from_attributes = True
        
class HomeResponse(BaseModel):
    message: str
    status: str = "ok"
    service: str = "approval_services"
    database: str = "rms_db"