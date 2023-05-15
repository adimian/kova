from functools import lru_cache
from pprint import pprint
from typing import Any

from pydantic import (
    BaseSettings,
    PostgresDsn,
    validator,
    RedisDsn,
    HttpUrl,
    Field,
)

ENV_FILE = ".env"


class Database(BaseSettings):
    class Config:
        env_prefix = "database_"
        env_file = ENV_FILE

    pool_pre_ping: bool = True
    pool_size: int = 10
    pool_max_overflow: int = 0
    echo: bool = False
    encryption_keys: list[str] = []

    host: str = "localhost"
    user: str = "kova-test"
    port: str = "5432"
    password: str = "kova-test"
    name: str = "kova-test"
    uri: PostgresDsn = ""

    @validator("uri", pre=True)
    def assemble_db_connection(
        cls,
        v: str | None,
        values: dict[str, Any],
    ) -> Any:
        if v:
            return v  # pragma: no cover
        else:
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("user"),
                port=values.get("port"),
                password=values.get("password"),
                host=values.get("host"),
                path=f"/{values.get('name') or ''}",
            )


class SMTP(BaseSettings):
    class Config:
        env_prefix = "smtp_"
        env_file = ENV_FILE

    hostname: str = "dev.localhost"
    port: int = 1025
    username: str = ""
    password: str = ""
    use_tls: bool = False
    dry_run: bool = True
    sender: str = "noreply@acme.test"


class Minio(BaseSettings):
    class Config:
        env_prefix = "minio_"
        env_file = ENV_FILE

    endpoint: str = "localhost:9001"
    bucket: str = "kova-test"
    region: str = "us-east-1"
    access_key: str = "minio"
    secret_key: str = "minio123"
    secure: bool = False


class Redis(BaseSettings):
    class Config:
        env_prefix = "redis_"
        env_file = ENV_FILE

    url: RedisDsn = "redis://localhost:6379"
    namespace: str = "kova-test"
    ssl_ca_certs: str | None = None


class Settings(BaseSettings):
    class Config:
        env_file = ENV_FILE

    debug: bool = False
    testing: bool = False
    env: str = "dev"
    redis: Redis = Field(default_factory=Redis)
    database: Database = Field(default_factory=Database)
    smtp: SMTP = Field(default_factory=SMTP)
    minio: Minio = Field(default_factory=Minio)

    capture_emails: bool = False

    nats_servers: str | list[str] = ["nats://localhost:4222"]

    nats_creds_directory: str | None = None

    sentry_dsn: HttpUrl | None = None


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings


def show():  # pragma: no cover
    settings = Settings()
    pprint(settings.dict())
