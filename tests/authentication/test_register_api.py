from sqlalchemy import select
import pytest

from kova.db.models import User


def test_user_can_register_with_their_email(client, session):
    res = client.post("/register", json={"email": "alice@acme.test"})
    assert res.status_code == 200, res.text

    result = session.execute(
        select(User).where(User.email == "alice@acme.test")
    )
    assert result.one()


def test_email_not_none(client, session):
    client.post("/register", json={"email": None})
    query = session.execute(select(User).where(User.email is None))
    user = query.one_or_none()
    assert user is None


def test_email_is_valid_email(client, session):
    client.post("/register", json={"email": "1234"})
    query = session.execute(select(User).where(User.email == "1234"))
    user = query.one_or_none()
    assert user is None


def test_user_can_register_once_only(client, session):
    res = client.post("/register", json={"email": "alice@acme.test"})
    assert res.status_code == 200, res.text

    with pytest.raises(ValueError):
        client.post("/register", json={"email": "alice@acme.test"})

    result = session.execute(
        select(User).where(User.email == "alice@acme.test")
    )
    assert result.one()
