from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import random_lower_string


def test_create_item(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
) -> None:
    item_data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=normal_user_token_headers,
        json=item_data,
    )

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Called endpoint: {settings.API_V1_STR}/items/"
    created_item = response.json()
    assert created_item["name"] == item_data["name"]
    assert created_item["description"] == item_data["description"]


def test_get_item(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    item_data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=normal_user_token_headers,
        json=item_data,
    )
    assert response.status_code == status.HTTP_200_OK, "Could not create an item"
    item = response.json()

    response = client.get(
        f"{settings.API_V1_STR}/items/{item['id']}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    retrieved_item = response.json()
    assert retrieved_item["id"] == item["id"]
    assert retrieved_item["name"] == item["name"]
    assert retrieved_item["description"] == item["description"]


def test_update_item(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
) -> None:
    item_data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=normal_user_token_headers,
        json=item_data,
    )
    assert response.status_code == status.HTTP_200_OK, "Could not create an item"
    item = response.json()

    update_data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.put(
        f"{settings.API_V1_STR}/items/{item['id']}",
        headers=normal_user_token_headers,
        json=update_data,
    )
    assert response.status_code == status.HTTP_200_OK
    updated_item = response.json()
    assert updated_item["id"] == item["id"]
    assert updated_item["name"] == update_data["name"]
    assert updated_item["description"] == update_data["description"]


def test_delete_item(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    item_data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=normal_user_token_headers,
        json=item_data,
    )
    assert response.status_code == status.HTTP_200_OK, "Could not create an item"
    item = response.json()

    response = client.delete(
        f"{settings.API_V1_STR}/items/{item['id']}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    deleted_item = response.json()
    assert deleted_item["id"] == item["id"]
    assert deleted_item["name"] == item["name"]
    assert deleted_item["description"] == item["description"]
