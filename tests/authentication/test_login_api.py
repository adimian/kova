def test_user_can_login_with_their_email(client, session):
    client.post("/register", json={"email": "alice@acme.test"})

    res = client.post("/login", json={"email": "alice@acme.test"})
    assert res.status_code == 200, res.json()


def test_user_not_register(client, session):
    res = client.post("/login", json={"email": "alice@acme.test"})
    assert res.status_code == 404, res.text


def test_user_no_email(client, session):
    res = client.post("/login", json={"email": None})
    assert res.status_code == 422, res.text
