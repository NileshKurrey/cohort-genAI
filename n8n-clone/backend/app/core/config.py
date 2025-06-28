try:
    from pydantic import BaseSettings
except ImportError:
    raise ImportError("pydantic is not installed. Please install it with 'pip install pydantic'.")

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
