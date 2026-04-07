from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

metadata = MetaData(
    schema="approval_service"
)

class Base(DeclarativeBase):
    metadata=metadata