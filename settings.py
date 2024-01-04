from pydantic import Field

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

SETTINGS = Settings()
