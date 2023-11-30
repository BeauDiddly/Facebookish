def test_register(client):
    client.post("/auth/register", data={
        "username": "Beaudemann2",
        "password": "ach",
        "confirm_password": "ach",
    })
    response = client.post("/auth/register", data={
        "username": "Beaudemann",
        "password": "ach",
        "confirm_password": "ach",
    })
    assert response.status_code == 200