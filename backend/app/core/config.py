from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/app"
    GROQ_API_KEY: str = ""
    SECRET_KEY: str = "your-secret-key-here"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:4173", "http://localhost:5174"]

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    SMTP_USE_TLS: bool = True


settings = Settings()
