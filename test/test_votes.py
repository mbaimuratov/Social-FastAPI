import pytest
from app import models

@pytest.fixture()
def setup_test_vote(test_posts, session):
    session.add(models.Vote(post_id=test_posts[2].id, user_id=1))
    session.commit()

def test_vote(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice(authorized_client, test_posts, setup_test_vote):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[2].id, "dir": 1})
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, setup_test_vote):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_not_found(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 404

def test_vote_post_not_found(authorized_client):
    res = authorized_client.post(f"/vote/", json={"post_id": 100, "dir": 1})
    assert res.status_code == 404

def test_unauthorized_vote(client, test_posts):
    res = client.post(f"/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401