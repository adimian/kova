from sqlalchemy import select

from kova.db.models import User


def test_user_can_register_with_their_email(client, session):
    res = client.post("/register", json={"email": "alice@acme.test"})
    assert res.status_code == 200, res.text

    result = session.execute(
        select(User).where(User.email == "alice@acme.test")
    )
    assert result.one()
