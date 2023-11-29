from app import db

def test_login(client):
    response = client.post("/auth/login", data={
        "username": "Beaudemann",
        "password": "ach",
    })
    assert response.status_code == 302

def test_register1(client):
    response = client.post("/auth/register", data={
        "username": "hungryboi",
        "password": "ach",
        "confirm_password": "ach",
    })
    db.session.delete()
    assert response.status_code == 302

def test_register2(client):
    response = client.post("/auth/register", data={
        "username": "Beaudemann",
        "password": "ach",
        "confirm_password": "ach",
    })
    assert response.status_code == 200