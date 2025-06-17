import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

LOG_DEFAULT_FORMAT = ("[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s")


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = logging.INFO
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]

class TaskIqConfig(BaseModel):
    url: AmqpDsn = "amqp://guest:guest@localhost:5672//"

class MailConfig(BaseModel):
    admin_email: str = "games_shop@mail.ru"
    hostname: str = 'localhost'
    port: int = 1025

class DbConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

class AuthJWT(BaseModel):
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 5
    refresh_token_expire_minutes: int = 42600
    public_key_path: Path = BASE_DIR / 'certs' / 'public_key.pem'
    private_key_path: Path = BASE_DIR / 'certs' / 'private_key.pem'

class MiddlewareConfig(BaseModel):
    allow_origins: list[str] = [
    "http://localhost",
    "http://localhost:8000"
    ]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_prefix='APP_CONFIG__',
                                      env_nested_delimiter='__',
                                      case_sensitive=False)
    db: DbConfig
    auth_jwt: AuthJWT = AuthJWT()
    logging_config: LoggingConfig = LoggingConfig()
    task_iq_config: TaskIqConfig = TaskIqConfig()
    mail_config: MailConfig = MailConfig()
    middleware_config: MiddlewareConfig = MiddlewareConfig()

settings = Settings()
