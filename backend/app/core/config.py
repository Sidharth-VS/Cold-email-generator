from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/app"
    GROQ_API_KEY: str = ""
    SECRET_KEY: str = "your-secret-key-here"

    class Config:
        env_file = ".env"


settings = Settings()
