from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    user_data = {
        "email": "test2@example.com",
        "password": "password123"
    }
    response = client.post("/users", json=user_data)
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == user_data["email"]
    