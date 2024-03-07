import pytest
from app import schemas


def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")

    def validate(post):
        return schemas.PostOutput(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorised_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorised_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorised_client):
    res = authorised_client.get(f"/posts/0000")
    assert res.status_code == 404


def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOutput(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("first title", "first content", True),
    ("second title", "second content", False),
    ("third title", "third content", True),
])
def test_create_post(authorised_client, test_user, title, content, published):
    res = authorised_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorised_client, test_user):
    res = authorised_client.post("/posts/", json={"title": "some title", "content": "some content"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "some title"
    assert created_post.content == "some content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={"title": "some title", "content": "some content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorised_client, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorised_client):
    res = authorised_client.delete(f"/posts/0000")
    assert res.status_code == 404


def test_delete_other_user_post(authorised_client, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorised_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorised_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorised_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorised_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorised_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    res = authorised_client.put(f"/posts/0000", json=data)

    assert res.status_code == 404
