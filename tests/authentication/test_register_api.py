import pytest
from kova.db.models import User
from sqlalchemy import select


@pytest.mark.anyio
async def test_user_can_register_with_their_email(client, session):
    res = client.post("/register", json={"email": "alice@acme.test"})
    assert res

    # s = await session

    result = await session.execute(
        select(User).where(User.email == "alice@acme.test")
    )
    assert result.one()
