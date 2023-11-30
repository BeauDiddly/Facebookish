def test_friends(client):
    client.post("/auth/login", data={
        "username": "Beaudemann",
        "password": "ach",
    })
    client.post("/auth/login", data={
        "username": "Beaudemann2",
        "password": "ach",
    }) 
    response = client.post("/friends/send_request", data={
        "friend": "Beaudemann",
    })
    assert response.status_code == 302