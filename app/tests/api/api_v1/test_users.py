from typing import Dict
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.user import authentication_token_from_email, create_random_user
from app.tests.utils.utils import random_email, random_lower_string


def test_api_users_get_me_as_admin(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    assert r.status_code == status.HTTP_200_OK
    current_user = r.json()
    assert current_user
    assert current_user["is_admin"] is True
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_api_users_get_me_as_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_admin"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def do_nothing(*args, **kwargs):
    return None


def test_api_users_create(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    with patch("fastapi.BackgroundTasks.add_task", side_effect=do_nothing):
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data,
        )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_api_users_get_by_id(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=user.email)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_api_users_create_with_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    password = random_lower_string()
    data = {"email": user.email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == status.HTTP_409_CONFLICT


def test_api_users_create_as_a_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_api_users_get_multiple(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    create_random_user(db)
    create_random_user(db)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item


def test_api_users_get_multiple_unauthorized(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/")
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


def test_api_users_get_multiple_as_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers)
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_api_users_archive(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user_before_archive = create_random_user(db)
    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_before_archive.id}/archive",
        headers=superuser_token_headers,
    )
    assert r.status_code == status.HTTP_200_OK
    user_after_archive_json = r.json()
    db.commit()
    user_after_archive = crud.user.get(
        db, id=user_after_archive_json["id"], with_archived=True
    )
    assert user_after_archive.id == user_before_archive.id
    assert user_after_archive.archived is True


def test_api_users_unarchive(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user_before_archive = create_random_user(db)
    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_before_archive.id}/archive",
        headers=superuser_token_headers,
    )
    db.commit()
    assert r.status_code == status.HTTP_200_OK
    user_before_archive = crud.user.get(
        db, id=user_before_archive.id, with_archived=True
    )
    assert user_before_archive.archived is True
    r = client.put(
        f"{settings.API_V1_STR}/users/{user_before_archive.id}/unarchive",
        headers=superuser_token_headers,
    )
    db.commit()
    user_after_unarchive = crud.user.get(
        db, id=user_before_archive.id, with_archived=True
    )
    assert r.status_code == status.HTTP_200_OK
    assert user_after_unarchive.archived is False


def test_api_users_archive_self(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    # WARNING: if the current test fails of fails partially it can yield an archived test user. To fix this log in to localhost/docs as an admin user and unarchive the test user.
    user = create_random_user(db)
    new_user_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    r = client.delete(
        f"{settings.API_V1_STR}/users/me/archive",
        headers=new_user_headers,
    )
    db.commit()
    user_after_archive = crud.user.get(db, id=user.id, with_archived=True)
    assert r.status_code == status.HTTP_200_OK
    assert user.id == user_after_archive.id
    assert user_after_archive.archived is True

    r = client.put(
        f"{settings.API_V1_STR}/users/{user.id}/unarchive",
        headers=superuser_token_headers,
    )
    db.commit()
    user_after_unarchive = crud.user.get(db, id=user.id, with_archived=True)
    assert r.status_code == status.HTTP_200_OK
    assert user.id == user_after_unarchive.id
    assert user_after_unarchive.archived is False
