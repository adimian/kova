import asyncio

import email_validator
import pytest
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
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


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def settings(event_loop):
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
async def engine(settings):
    settings = get_settings().database

    engine = create_async_engine(
        settings.uri,
        echo=settings.echo,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.pool_max_overflow,
    )
    yield engine
    await engine.dispose()


@pytest.fixture()
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine, create):
    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture
def app(
    session,
):
    app = app_maker()
    app.dependency_overrides[get_session] = lambda: session
    return app


@pytest.fixture
def client(app):
    return TestClient(app=app)
