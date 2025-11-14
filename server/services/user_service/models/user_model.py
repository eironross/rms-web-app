from datetime import datetime

from db.base_class import Base

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        unique=True,
        comment="Primary key of the User",
    )
    hashed_password: Mapped[str] = mapped_column(
        VARCHAR(97),
        nullable=False, 
        comment="Password of the user"
    )
    email: Mapped[str] = mapped_column(
        VARCHAR(225),
        nullable=True,
        comment="Company Email of the user"
    )
    
    is_active: Mapped[int ] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment= "Determines whether a user is active or not",
        server_default=text("TRUE")
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
    
    roles: Mapped[list["UserRoleModel"]] = relationship(
        secondary="user_xref",
        back_populates="users",
        lazy="selectin",
        passive_deletes=True
    )
    
    profile: Mapped["UserProfileModel"] = relationship(back_populates="user", lazy="selectin", passive_deletes=True, cascade="all, delete-orphan")

class UserProfileModel(Base):
    __tablename__ = "user_profiles"
    
    id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
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
    
    user: Mapped["UserModel"] = relationship(back_populates="profile", lazy="selectin", passive_deletes=True)
    
class UserJunctionModel(Base):
    __tablename__ = "user_xref"
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("user_roles.id", ondelete="CASCADE"),
         primary_key=True
    )
    

    
class UserRoleModel(Base):
    """user_role model table expected roles in first run will be:
        1 - admin
        2 - regulatory
        3 - trader
    """
    __tablename__ = "user_roles"
    
    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        comment="Primary key of the User",
    )
    
    role: Mapped[str] = mapped_column(
        VARCHAR(20),
        nullable=False,
        comment="Role of the user, admin, regulatory, user"
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

    users: Mapped[list["UserModel"]] = relationship(
        secondary="user_xref",
        back_populates="roles",
        lazy="selectin", 
        passive_deletes=True
    )