import os
from fastapi.testclient import TestClient
from app.main import app

# Set environment variable for testing
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'

client = TestClient(app)

def test_read_users_me():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "password"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me/", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "user"
