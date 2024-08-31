from app import schemas
from jose import jwt
from app.config import settings

def test_create_user(client):
    user_data = {
        "email": "test@gmail.com",
        "password": "test"
    }
    response = client.post("/users", json=user_data)
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == user_data["email"]
    
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert "token_type" in res.json()