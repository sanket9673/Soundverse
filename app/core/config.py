from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Soundverse Play Service"
    ENV: str = "development"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/soundverse_db"
    PORT: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()