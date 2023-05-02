def test_user_can_login_with_their_email(client, session):
    client.post("/register", json={"email": "alice@acme.test"})

    res = client.post("/login", json={"email": "alice@acme.test"})
    print(res)
    assert res.status_code == 200, res.text
