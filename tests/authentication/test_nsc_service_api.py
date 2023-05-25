import pytest
from starlette.testclient import TestClient
from loguru import logger

from pathlib import Path
import tempfile

from kova.authentication.nsc_api import (
    nsc_app_maker,
    NscSettings,
    get_nsc_settings,
)

from kova.authentication.nsc import NscException


@pytest.fixture
def test_nsc_settings():
    tmp = Path(tempfile.gettempdir()) / "nsc-creds"
    tmp.mkdir(exist_ok=True)
    return NscSettings(
        nats_creds_directory=tmp.as_posix(),
        operator_name="bobby",
        account_name="bob",
    )


@pytest.fixture
def nsc_client(test_nsc_settings):
    app = nsc_app_maker()
    app.dependency_overrides[get_nsc_settings] = lambda: test_nsc_settings
    return TestClient(app=app)


def test_client_working(nsc_client):
    res = nsc_client.get("/info")
    assert res.status_code == 200, res.text

    info = res.json()
    assert info["data_dir"] == "/tmp/nsc-creds/stores"


def test_set_up_operator_and_account(nsc_client):
    res = nsc_client.post(
        "/new-setup", json={"operator": "bobby", "account": "bob"}
    )
    assert res.status_code == 200, res.text


def test_create_user_credentials(nsc_client):
    res = nsc_client.post(
        "/new-user",
        json={"name": "123"},
    )
    assert res.status_code == 200, res.text

    credentials = res.json()
    logger.debug(f" User credentials : {credentials}")
    assert credentials.count(".") == 4


def test_set_up_new_account(nsc_client):
    res = nsc_client.post(
        "/new-setup", json={"operator": "bobby", "account": "alice"}
    )
    assert res.status_code == 200, res.text


def test_can_not_create_user_wrong_account(nsc_client):
    with pytest.raises(NscException):
        nsc_client.post(
            "/new-user",
            json={"name": "123", "account": "charlie"},
        )


def test_can_not_create_user_twice(nsc_client):
    with pytest.raises(NscException):
        nsc_client.post(
            "/new-user",
            json={"name": "123"},
        )
