import os
from fastapi.testclient import TestClient
from app.main import app

# Set environment variable for testing
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'

client = TestClient(app)

def test_get_token():
    response = client.post(
        "/token",
        data={"username": "user@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
