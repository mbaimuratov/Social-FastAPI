from app import schemas
import pytest

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    assert res.status_code == 200

def test_unauthorized_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_found(authorized_client, test_posts):
    res = authorized_client.get("/posts/100")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title
    assert post.post.content == test_posts[0].content
    assert post.post.owner_id == test_posts[0].owner_id

@pytest.mark.parametrize("title, content, publish", [("test3", "test3", True), ("test2", "test2", False)])
def test_create_post(authorized_client, test_user, title, content, publish):
    post = schemas.PostCreate(title=title, content=content, publish=publish)
    res = authorized_client.post("/posts/", json=post.dict())
    assert res.status_code == 201
    post = schemas.PostResponse(**res.json())
    assert post.owner_id == test_user["id"]

def test_unauthorized_create_post(client):
    post = schemas.PostCreate(title="test", content="test")
    res = client.post("/posts/", json=post.dict())
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_found(authorized_client):
    res = authorized_client.delete("/posts/100")
    assert res.status_code == 404

def test_delete_post_not_owner(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    post = schemas.PostUpdate(title="test_update_post", content="test_update_post")
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post.dict())
    assert res.status_code == 200
    post = schemas.PostUpdate(**res.json())
    assert post.title == "test_update_post"
    assert post.content == "test_update_post"

def test_update_post_not_owner(authorized_client, test_user, test_user2, test_posts):
    post = schemas.PostUpdate(title="test_update_post", content="test_update_post")
    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=post.dict())
    assert res.status_code == 403