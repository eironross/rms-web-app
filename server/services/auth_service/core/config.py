from sqlalchemy.engine import URL
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
    
class Settings(BaseSettings):
     
    # App Setting
    APP_NAME: str = "Authentication Services"
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
    
    #Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    
def get_setting() -> Settings:
    return Settings()

settings = get_setting()
    