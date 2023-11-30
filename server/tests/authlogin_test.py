from app import db
from app.models import User

def test_login(client):
    response = client.post("/auth/login", data={
        "username": "Beaudemann",
        "password": "ach",
    })
    assert response.status_code == 302


