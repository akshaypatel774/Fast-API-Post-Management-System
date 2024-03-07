import pytest
from app import models


@pytest.fixture()
def test_star(test_posts, session, test_user):
    new_star = models.Star(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_star)
    session.commit()


def test_star_on_post(authorised_client, test_posts):
    res = authorised_client.post("/star/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201


def test_star_twice_post(authorised_client, test_posts, test_star):
    res = authorised_client.post(
        "/star/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_star(authorised_client, test_posts, test_star):
    res = authorised_client.post(
        "/star/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_star_non_exist(authorised_client, test_posts):
    res = authorised_client.post(
        "/star/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404


def test_star_post_non_exist(authorised_client, test_posts):
    res = authorised_client.post(
        "/star/", json={"post_id": 0000, "dir": 1})
    assert res.status_code == 404


def test_star_unauthorized_user(client, test_posts):
    res = client.post(
        "/star/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401