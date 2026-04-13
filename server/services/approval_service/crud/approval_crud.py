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

from utility.approval_enum import (
    ApprovalQuery
    ,RoleName
    ,ApprovalStatusId
    ,ApprovalLevelId
)

from schemas.approval_schema import (
    ApprovalBase
    ,ApprovalAll
    ,ApprovalID
    ,ApprovalOut
    ,ApprovalReponse
    ,ApprovalUpdate
)

from core.logger import get_logger

USER_QUERY = text("""
            SELECT
                u.email,
                p.first_name,
                p.last_name,
                ur.role,
                ur.role_level
            FROM user_service.users u
            INNER JOIN user_service.user_profiles p ON p.id = u.id
            LEFT JOIN user_service.user_xref x ON x.user_id = u.id
            INNER JOIN user_service.user_roles ur ON ur.id = x.role_id
            WHERE
                 u.id = :user_id
                     """)


logger = get_logger(__name__)

async def submit_report(payload: ApprovalBase, db: AsyncSession) -> ApprovalOut:
    try: 
        
        ## Check the report_id exists in the Approval Request 1 report, 1 request
        report: ApprovalRequestModel = (await db.execute(select(ApprovalRequestModel)
                                       .where(
                                           ApprovalRequestModel.report_id == payload.report_id,
                                           ApprovalRequestModel.is_active == True
                                           ))).first()
        
        if report:
            raise HTTPException(status_code=400, detail="Report is already being processed for approval.")
                
        ## Get User
        user_details = (await db.execute(USER_QUERY, {"user_id": payload.created_by_id})).first()
                
        if user_details is None:
            raise HTTPException(status_code=404, detail="User can't be found.")
        
        if user_details.role.lower() != RoleName.ROLE_NAME:
            raise HTTPException(status_code=400, detail="A manager or team leader can't initiate the report approvalONLY energy trader can.")
        
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
            approval_level=new_approval.approvals.approval_requests.status,
            comment=new_approval.comment,
            created_by_id=new_approval.created_by_id,
            status_id=new_approval.status_id,
            status_name=new_approval.status.status_name
        )
        
    except Exception as e: 
        print(f"Error occured in {e}")
        raise


async def approve_report(payload: ApprovalBase, db: AsyncSession) -> ApprovalOut:
    try:  
        ## Check the report_id exists in the Approval Request 1 report, 1 request
        report: ApprovalRequestModel = (await db.execute(select(ApprovalRequestModel)
                                        .where(
                                           ApprovalRequestModel.report_id == payload.report_id,
                                           ApprovalRequestModel.is_active == True
                                           ))).first()
                                            
        
        if report is None:
            raise HTTPException(status_code=400, detail="Report can't be found")

        # Fetch User details from the user_service to determine the user_roles
        user_details = (await db.execute(USER_QUERY, {"user_id": payload.created_by_id})).first()
        
        if user_details is None:
            raise HTTPException(status_code=404, detail="User can't be found.")
        
        # Determine the current level of the approval
        current_level = report.approval_requests.approval_level
        
        logger.info(f"User current level is {current_level}")
        
        # Validate of the approval_level and role_level matches if matches the report status will be updated. Else throw an error.
        if current_level != user_details.role_level:
            raise HTTPException(status_code=400, detail="Can't Approve the report. You may have not have any privileges or the Hierarchy of Approval isn't Correct. Current Level is {current_level}")
            
        # Determine the status of the report
        status_id = ApprovalStatusId.UPDATED_STATUS
        
        # Determine the next level of the approval process    
        next_level = ApprovalLevelId(current_level).next_level
        
        if next_level == ApprovalLevelId.CLOSED:
            status_id = ApprovalStatusId.COMPLETED_STATUS
        
        if next_level:
            
            # Updates the request status
            report.approval_level_id = next_level
            
            # Create new item for the approval history
            new_approval: ApprovalHistory = ApprovalHistory(
                    description=f"Updated report status and approval by {user_details.first_name} {user_details.last_name}",
                    comment=payload.comment,
                    request_id=report.id,
                    status_id=status_id,
                    created_by_id=payload.created_by_id,
                )
            
            db.add(new_approval) 
            await db.commit()
            await db.refresh(new_approval)
            
            return ApprovalOut(
                    id=new_approval.id,
                    description=new_approval.description,
                    report_id=new_approval.approvals.report_id,
                    approval_level_id=new_approval.approvals.approval_level_id,
                    approval_level=new_approval.approvals.approval_requests.status,
                    comment=new_approval.comment,
                    created_by_id=new_approval.created_by_id,
                    status_id=new_approval.status_id,
                    status_name=new_approval.status.status_name
                )
        return {"message": "Report was already approved by management. Please submit the report to the agencies"}
        
        
    except Exception as e: 
        print(f"Error occured in {e}")
        raise
    
async def reject_or_return_report(payload: ApprovalBase, db: AsyncSession) -> ApprovalOut:
    try:    
        
        if payload.approval_level_id > ApprovalLevelId.RETURN_TO_SUBMITTER:
            raise HTTPException(status_code=400, detail="Wrong path you can't approve on this path. Only Reject or Return to Submitter")
        
        report: ApprovalRequestModel = (await db.execute(select(ApprovalRequestModel)
                                        .where(ApprovalRequestModel.report_id == payload.report_id))).scalar_one_or_none()
        
        if report is None:
            raise HTTPException(status_code=400, detail="Report can't be found")
        
        # Fetch User details from the user_service to determine the user_roles
        user_details = (await db.execute(USER_QUERY, {"user_id": payload.created_by_id})).first()
        
        if user_details is None:
            raise HTTPException(status_code=404, detail="User can't be found.")
        
        # Determine the current level of the approval
        current_level = report.approval_requests.approval_level
        
        logger.info(f" Current level is {current_level}")
        
        # Validate of the approval_level and role_level matches if matches the report status will be updated. Else throw an error.
        if current_level != user_details.role_level:
            raise HTTPException(status_code=400, detail="Can't Approve the report. You may have not have any privileges or the Hierarchy of Approval isn't Correct. Current Level is {current_level}")
        
        
        if payload.approval_level_id == ApprovalLevelId.REJECTED:
            report.approval_level_id = ApprovalLevelId.REJECTED
            report.is_active = False
            status_id = ApprovalStatusId.REJECTED_STATUS
        
        else:
            report.approval_level_id = current_level - 1
            status_id = ApprovalStatusId.RETURN_TO_SUBMITTER_STATUS
            
            
        new_approval: ApprovalHistory = ApprovalHistory(
                    description=f"Report status changed by {user_details.first_name} {user_details.last_name}, {status_id}",
                    comment=payload.comment,
                    request_id=report.id,
                    status_id=status_id,
                    created_by_id=payload.created_by_id,
                )
            
        db.add(new_approval)  
        await db.commit()
        await db.refresh(new_approval)
        
        return ApprovalOut(
                    id=new_approval.id,
                    description=new_approval.description,
                    report_id=new_approval.approvals.report_id,
                    approval_level_id=new_approval.approvals.approval_level_id,
                    approval_level=new_approval.approvals.approval_requests.status,
                    comment=new_approval.comment,
                    created_by_id=new_approval.created_by_id,
                    status_id=new_approval.status_id,
                    status_name=new_approval.status.status_name
                )       
        
    except Exception as e: 
        print(f"Error occured in {e}")
        raise
