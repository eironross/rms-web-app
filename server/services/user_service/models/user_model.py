from datetime import datetime

from pydantic import EmailStr, PositiveInt
from db.base_class import Base

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[PositiveInt] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        unique=True,
        comment="Primary key of the User",
    )
    first_name: Mapped[str] = mapped_column(
        VARCHAR(225), 
        nullable=False,
        comment="First Name of the User"
    )
    last_name: Mapped[str] = mapped_column(
        VARCHAR(225), 
        nullable=False,
        comment="Last Name of the User"
    )
    hashed_password: Mapped[str] = mapped_column(
        VARCHAR(97),
        nullable=False, 
        comment="Password of the user"
    )
    email: Mapped[EmailStr] = mapped_column(
        VARCHAR(225),
        nullable=True,
        comment="Company Email of the user"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True
        ),
        default=datetime.now(),
        nullable=False,
        server_default=text("now()"),
        comment="Time the User was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True
        ),
        nullable=True,
        onupdate=text("now()"),
        comment="Time the User was updated",
    )
    