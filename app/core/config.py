from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_POOLER: str
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASS: str
    DATABASE_URL: str
    DATABASE_KEY: str

    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    EMAIL_USER: str
    EMAIL_PASS: str

    REDIS_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
