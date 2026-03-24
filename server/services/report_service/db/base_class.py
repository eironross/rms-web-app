from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

metadata = MetaData(
    schema="report_service"
)

class Base(DeclarativeBase):
    metadata=metadata