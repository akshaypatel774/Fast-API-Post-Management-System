import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post("/users/", json={"email": "abc123@gmail.com", "password": "1234"})
    new_user = schemas.UserResponse(**res.json())

    assert new_user.email == "abc123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', '1234', 403),
    ('abc123@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, '1234', 422),
    ('abc123@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code