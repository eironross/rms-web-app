from datetime import datetime, date, time

from db.base_class import Base


from sqlalchemy import ForeignKey, text, func
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR, BOOLEAN, DATE, TIME, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the User",
    )
    
    title: Mapped[str] = mapped_column(
        VARCHAR(225),
        nullable=True,
        comment="Company Email of the user",
    )
    
    event_type_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=False,
        comment="Event Type Id like Synchronization, Forge Outage or Planned Outage"
    )
    
    
    report_details: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        comment="Report details on what happen on the Power Plant",
        server_default=text("'Lorem Ipsum'")
    )
    
    event_date: Mapped[date] = mapped_column(
        DATE,
        nullable=False,
        comment="Date for when the event occured",
        server_default=func.current_date()
    )
    
    event_time: Mapped[time] = mapped_column(
        TIME,
        nullable=False,
        comment="Time for when the event occured",
        server_default=func.current_time()
    )
    
    status_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=False,
        comment="Status of the report, New, Pending or Submitted"
    )
    
    unit_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=False,
        comment="Unit id reprensenting the Unit by 01FHRI_G01"
    )
    
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a report is active or not",
        server_default=text("TRUE")
    )
    
    created_by_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=False,
        comment="User Id for who created the report"
    )
    
    modified_by_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=False,
        comment="User Id for who modified the report"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True
        ),
        nullable=False,
        server_default=func.now(),
        comment="Time the User was created",
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True
        ),
        nullable=True,
        onupdate=func.now(),
        comment="Time the User was updated",
    )
    
  
