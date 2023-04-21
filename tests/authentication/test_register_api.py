import pytest
from kova.db.models import User


@pytest.mark.asyncio
async def test_user_can_register_with_their_email(client, session):
    res = client.post("/register", json={"email": "alice@acme.test"})
    assert res

    with await session as s:
        assert await s.query(User).filter(email="alice@acme.test").one()
