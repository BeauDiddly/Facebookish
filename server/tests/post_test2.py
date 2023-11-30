def test_post(client):
    client.post("/auth/login", data={
        "username": "Beaudemann",
        "password": "ach",
    })
    response = client.post("/post/create", data={
        "posttext": "Your mother is a nice lady",
    })
    assert response.status_code == 302