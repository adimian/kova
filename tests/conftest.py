import email_validator
import pytest
from cryptography.fernet import Fernet

from kova.router import InMemoryQueue, Context
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
def ctx():
    return Context()


@pytest.fixture
def queue():
    return InMemoryQueue()
