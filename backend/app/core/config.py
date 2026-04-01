from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEBUG: bool = False
    APP_NAME: str = "Price Monitor API"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
