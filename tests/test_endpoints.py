from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_users_me():
    response = client.post(
        "/token",
        data={"username": "human@example.com", "password": "569569"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    print(f"DEBUG: Access token {token}")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me/", headers=headers)
    print(f"DEBUG: /users/me/ response {response.json()}")
    assert response.status_code == 200
    assert response.json()["email"] == "human@example.com"
    assert response.json()["username"] == "human"
    assert response.json()["full_name"] == "Human Being"
