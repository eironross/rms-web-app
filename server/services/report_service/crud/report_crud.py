## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from pydantic import EmailStr

## Service Import
from models.report_model import (ReportModel, 
                                 StatusModel, 
                                 EventTypeModel, 
                                 UnitNoModel)

from schemas.report_schema import (HomeResponse, 
                                   ReportAll, 
                                   ReportID, 
                                   ReportOut, 
                                   ReportBase, 
                                   ReportReponse, 
                                   ReportUpdate)

async def get_report(id: int, username: str,  db: AsyncSession) -> ReportOut:
    try:
        result = (await db.execute(
            select(ReportModel).where(ReportModel.id == id)
        )).scalar_one_or_none()
        
        if result is None:
            raise HTTPException(status_code=404, detail="User can't be found.")
        
        return ReportOut(
            id=result.id,
            title=result.title,
            event_type_id=result.event_type_id,
            report_details=result.report_details,
            status_id=result.status_id,
            unit_id=result.unit_id,
            event_date=result.event_date,
            event_time=result.event_time,
            created_by=username,
            created_at=result.created_at
        )
        
    except Exception as e: 
        print(f"Error occured in {e}")
        raise

async def get_all_report(db: AsyncSession, page: int = 1, size: int = 10)-> ReportAll:
    try:
        offset = (page - 1) * size
        total_count = (await db.execute(
            select(func.count(ReportModel.id))
        )).scalar()
        
        result = (await db.execute(
            select(ReportModel)
            .options(
                selectinload(ReportModel.status),
                selectinload(ReportModel.events), 
                selectinload(ReportModel.units)
            )
            .offset(offset).limit(size)
        )).scalars().all()
        print(result)
        print(len(result))
        
        reports = [ReportOut.model_validate({
            "id": u.id,
            "title": u.profile.first_name,
            "unit_name": u.units.name, 
            "event_name": u.events.event_name,
            "status_name": u.status.status_name,
            "report_details": u.report_details,
            "event_date": u.event_date,
            "event_time": u.event_time, 
        })
            for u in result]
    
        
        print(reports)
        return ReportAll(
            total_count=total_count, 
            page=page,
            size=size,
            reports=reports
        )
        
    except Exception as e:
        print(f"Error occured in {e}")
        raise 

async def create_report(username: str, payload: ReportBase, db: AsyncSession) -> ReportOut:
    try: 
        new_report = ReportModel(
            title=payload.title,
            event_type_id=payload.event_type_id,
            report_details=payload.report_details,
            status_id=payload.status_id,
            unit_id=payload.unit_id,
            event_date=payload.event_date,
            event_time=payload.event_time
        )
        
        db.add(new_report) 
        await db.commit()
        await db.refresh(new_report)
        
        return ReportOut(
            id=new_report.id,
            title=new_report.title,
            event_type_id=new_report.event_type_id,
            report_details=new_report.report_details,
            status_id=new_report.status_id,
            unit_id=new_report.unit_id,
            event_date=new_report.event_date,
            event_time=new_report.event_time,
            created_by=username,
            created_at=new_report.created_at
        )
    except Exception as e: 
        print(f"Error occured in {e}")
        raise
    
async def update_report(username: str, payload: ReportBase, db: AsyncSession) -> ReportOut:
    try:
        
        result = (await db.execute(
            select(ReportModel).where(ReportModel.id == id)
        )).scalar_one_or_none()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Report can't be found.")
        

        for key, value in payload.model_dump(exclude_unset=True, exclude={"first_name", "last_name", "role"}).items():
            setattr(result, key, value)
                        
        await db.commit()
        await db.refresh(result)
        
        return ReportOut(
            id=result.id,
            title=result.title,
            event_type_id=result.event_type_id,
            report_details=result.report_details,
            status_id=result.status_id,
            unit_id=result.unit_id,
            event_date=result.event_date,
            event_time=result.event_time,
            created_by=username,
            created_at=result.created_at
        )
        
    except Exception as e:
        print(f"Error occured in {e}")
        raise
    
async def delete_user(id: ReportID, db: AsyncSession) -> ReportID:
    try:
        result = (await db.execute(
            select(ReportModel).where(ReportModel.id == id)
        )).scalar_one_or_none()
        
        print(f"Return the report to {result}")
        
        if result is None:
            raise HTTPException(status_code=404, detail="Report can't be found.")
        
        await db.delete(result)
        await db.commit()
        
        return result
        
    except Exception as e:
        print(f"Error occured in {e}")
        raise