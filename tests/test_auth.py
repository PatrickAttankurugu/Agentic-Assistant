from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_token():
    response = client.post(
        "/token",
        data={"username": "human@example.com", "password": "569569"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
