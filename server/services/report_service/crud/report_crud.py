## Dependnecies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from pydantic import EmailStr

from core.logger import get_logger

logger = get_logger(__name__)
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


QUERY = text("""
            SELECT
                r.*
                ,s.status_name
                ,e.event_name
                ,o.name 
                ,u.email
            FROM report_service.reports r
            INNER JOIN report_service.status s ON s.id = r.status_id
            INNER JOIN report_service.event_types e ON e.id = r.event_type_id
            INNER JOIN report_service.operating_units o ON o.id = r.unit_id
            INNER JOIN user_service.users u ON u.id = r.created_by_id
            WHERE
                (:report_id IS NULL OR r.id = :report_id)
                     """)

QUERY_ALL = text("""
            SELECT
                r.*
                ,s.status_name
                ,e.event_name
                ,o.name 
                ,u.email
            FROM report_service.reports r
            INNER JOIN report_service.status s ON s.id = r.status_id
            INNER JOIN report_service.event_types e ON e.id = r.event_type_id
            INNER JOIN report_service.operating_units o ON o.id = r.unit_id
            INNER JOIN user_service.users u ON u.id = r.created_by_id
            ORDER BY r.id
            LIMIT :limit OFFSET :offset
                     """) 

async def get_report(id: int, db: AsyncSession) -> ReportOut:
    try:
        result = (await db.execute(QUERY, {"report_id": id})).first()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Report can't be found.")
                
        logger.info(f"Return the {result}") 
        
    
        return ReportOut(**result._mapping)

    except Exception as e: 
        print(f"Error occured in {e}")
        raise

async def get_all_report(db: AsyncSession, page: int = 1, size: int = 10)-> ReportAll:
    try:
        ## potentially to error if db wasnt initialliszed
        offset = (page - 1) * size
        total_count = (await db.execute(
            select(func.count(ReportModel.id))
        )).scalar()
        
        result = await db.execute(QUERY_ALL, {"limit": size, "offset": offset})
        
        if result is None:
            raise HTTPException(status_code=404, detail="Report can't be found.")
    
        reports = [ReportOut(**row) for row in result.mappings()]
        
        logger.info(reports[0])
        return ReportAll(
            total_count=total_count, 
            page=page,
            size=size,
            reports=reports
        )
        
    except Exception as e:
        print(f"Error occured in {e}")
        raise 

async def create_report(payload: ReportBase, db: AsyncSession) -> ReportOut:
    try: 
        
        name = (await db.execute(select(EventTypeModel)
                                       .where(EventTypeModel.id == payload.status_id))).scalar_one_or_none()
        
        new_report = ReportModel(
            title=f"{payload.title} {name.event_name}",
            event_type_id=payload.event_type_id,
            report_details=payload.report_details,
            status_id=payload.status_id,
            unit_id=payload.unit_id,
            created_by_id=payload.created_by_id,
            event_date=str(payload.event_date),
            event_time=str(payload.event_time)
        )
        
        db.add(new_report) 
        await db.commit()
        await db.refresh(new_report)
        
        result = await db.execute(QUERY, {"report_id": new_report.id})
        
        row = result.first()
        
        logger.info(f"Return the {row} This is the obj {result}") 
        
        if row:
            return ReportOut(**row._mapping)
        
    except Exception as e: 
        print(f"Error occured in {e}")
        raise
    
async def update_report(id: int, payload: ReportBase, db: AsyncSession) -> ReportOut:
    try:
        
        result = (await db.execute(
            select(ReportModel).where(ReportModel.id == id)
        )).scalar_one_or_none()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Report can't be found.")
        

        for key, value in payload.model_dump(exclude_unset=True, exclude={"id"}).items():
            setattr(result, key, value)
                        
        await db.commit()
        await db.refresh(result)
        
        result = await db.execute(QUERY, {"report_id": result.id})
        
        row = result.first()
        
        logger.info(f"Return the {row} This is the obj {result}") 
        
        if row:
            return ReportOut(**row._mapping)

        
        
    except Exception as e:
        print(f"Error occured in {e}")
        raise
    
async def delete_report(id: ReportID, db: AsyncSession) -> ReportID:
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