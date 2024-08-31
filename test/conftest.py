from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base
from app import schemas
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user = schemas.UserCreate(email="test@gmail.com", password="test")
    res = client.post("/users", json=user.dict())
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user.password
    return new_user

@pytest.fixture
def test_user2(client):
    user = schemas.UserCreate(email="test2@gmail.com", password="test")
    res = client.post("/users", json=user.dict())
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user.password
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers["Authorization"] = f"Bearer {token}"
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    session.add_all([models.Post(title="test1", content="test1", owner_id=test_user["id"]), 
                    models.Post(title="test2", content="test2", owner_id=test_user["id"]),
                    models.Post(title="test3", content="test3", owner_id=test_user2["id"])
                    ])
    session.commit()

    return session.query(models.Post).all()