from sqlalchemy import create_engine, inspect
import asyncio

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

async def check_table_deeply(table_name: str, schema: str = "report_service"):
    inspector = await inspect(engine)
    # has_table returns True if found, False otherwise
    return inspector.has_table(table_name, schema=schema)

# Example usage
exists = check_table_deeply("event_reports")
print(f"Table exists: {exists}")