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
        nullable=False,
        comment="Company Email of the user",
    )
    
    event_type_id: Mapped[int] = mapped_column(
        ForeignKey("report_service.event_types.id"), 
        nullable=False,
        comment="Event Type Id like Synchronization, Forge Outage or Planned Outage"
    )
    
    report_details: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        comment="Report details on what happen on the Power Plant",
        server_default=text("'Lorem Ipsum'")
    )
    
    event_date: Mapped[str] = mapped_column(
        VARCHAR(15),
        nullable=False,
        comment="Date for when the event occured",
        server_default=text("'9999-99-99'")
    )
    
    event_time: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        comment="Time for when the event occured",
        server_default=text("'24:00'")
    )
    
    status_id: Mapped[int] = mapped_column(
        ForeignKey("report_service.status.id"),
        nullable=False,
        comment="Status of the report, New, Pending or Submitted"
    )
    
    unit_id: Mapped[int] = mapped_column(
        ForeignKey("report_service.operating_units.id"),
        nullable=False,
        comment="Unit id reprensenting the Unit by 01FHRI_G01"
    )
    
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a report is active or not",
        server_default=text("'TRUE'")
    )
    
    created_by_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=False,
        comment="User Id for who created the report"
    )
    
    modified_by_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=True,
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
        server_default=func.now(),
        comment="Time the User was updated",
    )

    status: Mapped["StatusModel"] = relationship(back_populates="reports", lazy="selectin", passive_deletes=True, cascade="save-update, merge, refresh-expire, expunge")
    events: Mapped["EventTypeModel"] = relationship(back_populates="reports", lazy="selectin", passive_deletes=True,cascade="save-update, merge, refresh-expire, expunge")
    units: Mapped["UnitNoModel"] = relationship(back_populates="reports", lazy="selectin", passive_deletes=True,cascade="save-update, merge, refresh-expire, expunge")

class StatusModel(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the table"
    )

    status_code: Mapped[str] = mapped_column(
        VARCHAR(2),
        nullable=False,
        server_default=text("'N/A'"),
        comment="Code statuses for the reports"
    )

    status_name: Mapped[str] = mapped_column(
        VARCHAR(25),
        nullable=False,
        server_default=text("'N/A'"),
        comment="Status name for the report"
    )

    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a field is active or not",
        server_default=text("'TRUE'")
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
        server_default=func.now(),
        comment="Time the User was updated",
    )

    reports: Mapped["ReportModel"] = relationship(back_populates="status", lazy="selectin", passive_deletes=True)

class EventTypeModel(Base):
    __tablename__ = "event_types"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the table"
    )

    event_code: Mapped[str] = mapped_column(
        VARCHAR(2),
        nullable=False,
        server_default=text("'N/A'"),
        comment="Event code for the reports"
    )

    event_name: Mapped[str] = mapped_column(
        VARCHAR(25),
        nullable=False,
        server_default=text("'N/A'"),
        comment="Event name for the report"
    )

    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a field is active or not",
        server_default=text("'TRUE'")
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
        server_default=func.now(),
        comment="Time the User was updated",
    )

    reports: Mapped["ReportModel"] = relationship(back_populates="events", lazy="selectin", passive_deletes=True)

class UnitNoModel(Base):
    __tablename__ = "operating_units"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the table"
    )

    resource_name: Mapped[str] = mapped_column(
        VARCHAR(15),
        nullable=False,
        server_default=text("'N/A'"),
        comment="Resource name equivalent from the Market Code"
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(25),
        nullable=False,
        server_default=text("'zzUnit test'"),
        comment="Unit name of the facility"
    )

    facility_id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        comment="Unit's facility id where the unit is location"
    )
    
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a field is active or not",
        server_default=text("'TRUE'")
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
        server_default=func.now(),
        comment="Time the User was updated",
    )

    reports: Mapped["ReportModel"] = relationship(back_populates="units", lazy="selectin", passive_deletes=True)
    
    
