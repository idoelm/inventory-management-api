from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Inventory Management API"
    API_V1_STR: str = "/api/v1"
    
    # בברירת מחדל משתמש ב-SQLite. בהמשך נחליף בקלות ל-PostgreSQL דרך קובץ env.
    DATABASE_URL: str = "sqlite:///./inventory.db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()