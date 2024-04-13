from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


def test_api_users_get_multiple_as_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    # Update current user language to french
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json={"language": "fr"},
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["language"] == "fr"
    r = client.get(f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers)
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert r.json() == {"detail": "L'utilisateur courant n'a pas assez de privilèges"}
