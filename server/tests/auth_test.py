from app import db
from app.models import User

def test_login(client):
    response = client.post("/auth/login", data={
        "username": "Beaudemann",
        "password": "ach",
    })
    assert response.status_code == 302


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