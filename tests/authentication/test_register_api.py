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


@pytest.mark.parametrize("email", [None, ""])
def test_email_not_none(client, session, email):
    res = client.post("/register", json={"email": email})
    assert res.status_code == 422, res.text

    query = session.execute(select(User).where(User.email is None))
    user = query.one_or_none()
    assert user is None


def test_user_can_register_once_only(client, session):
    res = client.post("/register", json={"email": "alice@acme.test"})
    assert res.status_code == 200, res.text

    res = client.post("/register", json={"email": "alice@acme.test"})
    assert res.status_code == 403, res.text

    result = session.execute(
        select(User).where(User.email == "alice@acme.test")
    )
    assert result.one()
