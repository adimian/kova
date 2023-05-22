def test_association_operator(client):
    res = client.get("/operator")
    assert res.status_code == 200, res.text
    assert res.json() == "operator-nats"
