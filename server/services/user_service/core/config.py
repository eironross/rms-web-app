from sqlalchemy.engine import URL
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
    
class Settings(BaseSettings):
     
    # App Setting
    APP_NAME: str = "User Services"
    APP_VERSION: str = "1.0.0"
    
    # Databases
    DATABASE_URL: URL = URL.create(
    drivername=os.environ.get("POSTGRES_DRIVER"),
    username=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    host=os.environ.get("POSTGRES_HOST"),
    port=os.environ.get("POSTGRES_PORT"),
    database=os.environ.get("POSTGRES_DB"),
    )
    
    # External Services
    AUTH_SERVICE_URL: str = os.environ.get("AUTH_SERVICE_URL")
    
def get_setting() -> Settings:
    return Settings()

settings = get_setting()
    