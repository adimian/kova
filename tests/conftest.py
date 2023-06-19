import email_validator
import pytest
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.ddl import DropSchema, CreateSchema
from starlette.testclient import TestClient

from minio import Minio

from kova.authentication import app_maker, get_nsc_client, TestNscClient
from kova.db import Base
from kova.db import get_session
from kova.router import InMemoryQueue
from kova.server import Server
from kova.settings import get_settings

email_validator.SPECIAL_USE_DOMAIN_NAMES.remove("test")


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

    engine = create_engine(
        settings.uri,
        echo=settings.echo,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.pool_max_overflow,
    )

    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def session(engine, settings, worker_id):
    schema = f"_s_{worker_id}"

    try:
        with engine.begin() as connection:
            connection.execute(DropSchema(schema, cascade=True))
    except ProgrammingError:
        pass  # schema properly deleted
    finally:
        with engine.begin() as connection:
            connection.execute(CreateSchema(schema))

    tmp_engine = engine.execution_options(schema_translate_map={None: schema})

    session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=tmp_engine
    )
    db = session_local()
    engine.echo = settings.database.echo

    Base.metadata.drop_all(bind=tmp_engine)

    try:
        Base.metadata.create_all(bind=tmp_engine)
        db.execute(text(f"SET search_path TO {schema}"))
        yield db
    finally:
        db.rollback()
        tmp_engine.echo = False
        Base.metadata.drop_all(bind=tmp_engine)
        with engine.begin() as connection:
            connection.execute(DropSchema(schema))


@pytest.fixture
def app(
    session,
):
    app = app_maker()
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_nsc_client] = lambda: TestNscClient()
    return app


@pytest.fixture
def client(app):
    return TestClient(app=app)


@pytest.fixture
def minio(settings):
    client = Minio(
        settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure,
    )
    return client
