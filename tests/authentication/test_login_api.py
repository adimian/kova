import pytest


def test_user_can_login_with_their_email(client, session):
    client.post("/register", json={"email": "alice@acme.test"})

    res = client.get("/login/alice@acme.test")
    # print(res.json())
    assert res.status_code == 200, res.json()


def test_user_not_register(client, session):
    with pytest.raises(ValueError):
        client.get("/login/alice@acme.test")


def test_user_no_email(client, session):
    res = client.get("/login/")
    assert res.status_code == 404, res.text
