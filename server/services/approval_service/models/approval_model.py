from datetime import datetime, date, time
from typing import List

from db.base_class import Base

from sqlalchemy import ForeignKey, text, func
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR, BOOLEAN, DATE, TIME, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utility.approval_enum import ApprovalLevelId

class ApprovalLevelModel(Base):
    __tablename__ = "approval_hierarchy"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the approval level",
    )
    
    status: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Status of the Approval",
    )
    
    rolename: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Role of theu user Trader, Admin, Manager",
    )
    
    approval_level: Mapped[str] = mapped_column(
        INTEGER,
        nullable=False,
        comment="Level of the approval",
    )
    
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a approval level is active or not",
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
    
    approval_levels: Mapped["ApprovalRequestModel"] =  relationship(back_populates="approval_requests", lazy="selectin", passive_deletes=True)
    
class ApprovalRequestModel(Base):
    __tablename__ = "approval_request"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the approval request",
    )
    
    approval_level_id: Mapped[int] = mapped_column(
        ForeignKey("approval_service.approval_hierarchy"),
        nullable=False,
        default=ApprovalLevelId.SENIOR_ENERGY_TRADER,
        comment="Id that can be combined with the approval_level table"
    )

    report_id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        comment="Logical link to report_service.reports.id"
    )
    
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a approval level is active or not",
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
    
    approval_histories: Mapped[List["ApprovalHistory"]] = relationship(back_populates="approvals", lazy="selectin", passive_deletes=True)
    approval_requests: Mapped["ApprovalLevelModel"] = relationship(back_populates="approval_levels", lazy="selectin", passive_deletes=True)
    
class ApprovalHistory(Base):
    __tablename__ = "approval_history"
    
    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the approval history",
    )
    
    request_id: Mapped[int] = mapped_column(
        ForeignKey("approval_service.approval_request.id"),
        nullable=False,
        comment="Approval Request that mapped back to the report linked to it"
    )
    
    description: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=True,
        comment="description of the approval with current role who is interacting on the report"
    )
    
    comment: Mapped[str] =  mapped_column(
        TEXT,
        nullable=True,
        comment="Where user can add comment on the report"    
    )
    
    status_id: Mapped[str] = mapped_column(
        ForeignKey("approval_service.approval_status.id"),
        nullable=False,
        comment="Status of the approval, New, Completed, Updated, Rejected, Return to Submitter"
    )
    
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a approval level is active or not",
        server_default=text("'TRUE'")
    )
    
    created_by_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=False,
        comment="User Id for who created the level"
    )
    
    modified_by_id: Mapped[int] = mapped_column(
        INTEGER, 
        nullable=True,
        comment="User Id for who modified the level"
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
    )
    
    approvals: Mapped["ApprovalRequestModel"] = relationship(back_populates="approval_histories", lazy="selectin", passive_deletes=True, cascade="save-update, merge, refresh-expire, expunge")
    status: Mapped["ApprovalStatusModel"] = relationship(back_populates="approval_histories", lazy="selectin", passive_deletes=True, cascade="save-update, merge, refresh-expire, expunge")
    

class ApprovalStatusModel(Base):
    __tablename__ = "approval_status"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        comment="Primary key of the table"
    )

    status_name: Mapped[str] = mapped_column(
        VARCHAR(100),
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
    
    approval_histories: Mapped["ApprovalHistory"] = relationship(back_populates="status", lazy="selectin", passive_deletes=True)