from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Soundverse Play Service"
    ENV: str = "development"
    DATABASE_URL: str
    PORT: int = 8000
    API_KEY: str = "soundverse-secret-key-2026"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()