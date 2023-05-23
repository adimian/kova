import pytest
from starlette.testclient import TestClient
from loguru import logger

from kova.nsc_api import nsc_app_maker


@pytest.fixture
def nsc_client():
    app = nsc_app_maker()
    return TestClient(app=app)


def test_set_up_operator_and_account(nsc_client):
    res = nsc_client.post(
        "/new-setup", json={"operator": "bobby", "account": "bob"}
    )
    assert res.status_code == 200, res.text
    logger.debug(res.json())
