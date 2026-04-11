## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from pydantic import EmailStr

from models.approval_model import (
    ApprovalLevelModel
    ,ApprovalHistory
    ,ApprovalRequestModel
    ,ApprovalStatusModel)

from schemas.approval_schema import (
    ApprovalBase
    ,ApprovalAll
    ,ApprovalID
    ,ApprovalOut
    ,ApprovalReponse
    ,ApprovalUpdate
)

from core.logger import get_logger

logger = get_logger(__name__)

ROLE_NAME = "trader"

USER_QUERY = text("""
            SELECT
                u.email,
                p.first_name,
                p.last_name,
                ur.role
            FROM user_service.users u
            INNER JOIN user_service.user_profiles p ON p.id = u.id
            LEFT JOIN user_service.user_xref x ON x.user_id = u.id
            INNER JOIN user_service.user_roles ur ON ur.id = x.role_id
            WHERE
                 u.id = :user_id
                     """)


async def submit_report(payload: ApprovalBase, db: AsyncSession) -> ApprovalOut:
    try: 
        
        ## Check the report_id exists in the Approval Request 1 report, 1 request
        report = (await db.execute(select(ApprovalRequestModel)
                                       .where(ApprovalRequestModel.report_id == payload.report_id))).first()
        
        if report:
            raise HTTPException(status_code=400, detail="Report is already being processed for approval.")
                
        ## Approval Name
        approval_name = (await db.execute(select(ApprovalLevelModel)
                                       .where(ApprovalLevelModel.approval_level == payload.approval_level_id))).scalar_one_or_none()
        
        print(approval_name.approval_level)
        ## Get User
        user_details = (await db.execute(USER_QUERY, {"user_id": payload.created_by_id})).first()
        
        print(user_details)
        
        if user_details is None:
            raise HTTPException(status_code=404, detail="User can't be found.")
        
        if user_details.role.lower() != ROLE_NAME:
            raise HTTPException(status_code=400, detail="Wrong Input.")
        
        new_approval = ApprovalHistory(
            description=f"A new report was submitted for approval by {user_details.first_name} {user_details.last_name}",
            comment=payload.comment,
            status_id=payload.status_id,
            created_by_id=payload.created_by_id,
            approvals=ApprovalRequestModel(
                approval_level_id=payload.approval_level_id,
                report_id=payload.report_id
            )
        )
        
        db.add(new_approval) 
        await db.commit()
        await db.refresh(new_approval)

        return ApprovalOut(
            id=new_approval.id,
            description=new_approval.description,
            report_id=new_approval.approvals.report_id,
            approval_level_id=new_approval.approvals.approval_level_id,
            approval_level=approval_name.status,
            comment=new_approval.comment,
            created_by_id=new_approval.created_by_id,
            status_id=new_approval.status_id,
            status_name=new_approval.status.status_name
        )
        
    except Exception as e: 
        print(f"Error occured in {e}")
        raise
    