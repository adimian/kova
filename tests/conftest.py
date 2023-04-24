import email_validator
import pytest
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.testclient import TestClient

from kova.authentication import app_maker
from kova.db import Base
from kova.db import get_session
from kova.router import InMemoryQueue
from kova.server import Server
from kova.settings import get_settings

email_validator.SPECIAL_USE_DOMAIN_NAMES.remove("test")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def settings():
    settings = get_settings()
    settings.debug = True
    settings.testing = True
    settings.sentry_dsn = None
    settings.database.encryption_keys = [Fernet.generate_key()]

    return settings


@pytest.fixture
def server(settings):
    return Server(settings=settings)


@pytest.fixture
def queue():
    return InMemoryQueue()


@pytest.fixture
def worker_id(request):
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    else:
        return "default"


@pytest.fixture(scope="session")
def engine(settings):
    settings = get_settings().database

    engine = create_async_engine(
        settings.uri,
        echo=settings.echo,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.pool_max_overflow,
    )

    yield engine


@pytest.fixture(scope="function")
async def session(engine, settings):
    async_session = async_sessionmaker(bind=engine)
    engine.echo = settings.database.echo

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with async_session() as session:
            yield session
    finally:
        engine.echo = False
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def app(
    session,
):
    app = app_maker()
    app.dependency_overrides[get_session()] = lambda: session
    return app


@pytest.fixture
def client(app):
    return TestClient(app=app)
