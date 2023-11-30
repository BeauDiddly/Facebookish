from pathlib import Path
resources = Path(__file__).parent / "resources"



def test_postimage(client):
    client.post("/auth/login", data={
        "username": "Beaudemann",
        "password": "ach",
    })
    response = client.post("/post/create", data={
        "posttext": "Your mother is a nice lady",
        "image": (resources / "F_EhV1YbQAAYdN2.png").open("rb"),
    })
    assert response.status_code == 302