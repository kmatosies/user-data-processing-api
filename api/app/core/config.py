from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "User Data Processing API"
    database_url: str = "sqlite:///./app.db"


settings = Settings()
