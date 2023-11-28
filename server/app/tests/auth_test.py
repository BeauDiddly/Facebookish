
def test_login(client):
    response = client.post("/login", data={
        "username": "Beau",
        "password": "swagmonster",
    })
    assert response.status_code == 200