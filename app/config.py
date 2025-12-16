from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # Application
    app_name: str = "Personal-Finance-Tracker-API"
    debug: bool = False
    api_v1_str: str = "/api/v1"
    
    # Security
    secret_key: str  # ← No default, must come from .env
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str  # ← No default, must come from .env
    db_echo: bool = False
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    ) # type: ignore


settings = Settings()  # type: ignore
