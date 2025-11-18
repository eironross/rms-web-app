from sqlalchemy.engine import URL
import os


def create_url():
    return URL.create(
    drivername=os.environ.get("POSTGRES_DRIVER"),
    username=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    host=os.environ.get("POSTGRES_HOST"),
    port=os.environ.get("POSTGRES_PORT"),
    database=os.environ.get("POSTGRES_DB"),
)