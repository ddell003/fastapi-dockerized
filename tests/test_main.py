from fastapi.testclient import TestClient
from api.config import config

base_prefix = "/api"


def build_api_path(path_part: str):
    return f"{config.api_prefix}{path_part}"


def test_get_all_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0
    assert body["data"][0]["id"]


def test_get_roles(client):
    response = client.get("/api/roles")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_docs(client):
    response = client.get(build_api_path("/"))
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"


def test_get_user_not_found(client):
    response = client.get(f"{config.api_prefix}/users/250")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user(client):
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@gmail.com",
        "active": True,
    }
    response = client.put(build_api_path(f"/users/{1}"), json=user_data)
    assert response.status_code == 200
    user = dict(response.json())
    assert user.get("first_name") == "Alice"
    assert user.get("id") == 1


def test_update_user_invalid_package(client):
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@gmail.com",
        "active": True,
    }
    user_id = 1000
    response = client.put(build_api_path(f"/users/{user_id}"), json=user_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_invalid_request(client):
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@gmail.com",
    }
    user_id = 1
    response = client.put(build_api_path(f"/users/{user_id}"), json=user_data)
    assert response.status_code == 422


def test_can_filter_users_by_name_on_query_parameter(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 10

    queried_response = client.get("/api/users?q=alice")
    assert queried_response.status_code == 200
    assert len(queried_response.json()["data"]) == 2


def test_can_sort_users_on_query_parameter(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 10

    queried_response_asc = client.get("/api/users?sort=last_name&direction=asc")
    assert queried_response_asc.status_code == 200
    assert queried_response_asc.json()["data"][0]["last_name"] == "Alice"

    queried_response_desc = client.get("/api/users?sort=last_name&direction=desc")
    assert queried_response_desc.status_code == 200
    assert queried_response_desc.json()["data"][0]["last_name"] == "Zach"

    queried_response = client.get("/api/users?sort=last_name")
    assert queried_response.status_code == 200
    assert queried_response.json()["data"][0]["last_name"] == "Zach"


def test_can_sort_direction_parameter_requires_valid_value(client):

    queried_response = client.get("/api/users?sort=last_name&direction=bad")
    assert queried_response.status_code == 422


def test_can_sort_and_query_users(client):
    queried_response = client.get("/api/users?q=alice&sort=last_name")
    assert queried_response.status_code == 200
    assert len(queried_response.json()["data"]) == 2
    assert queried_response.json()["data"][0]["first_name"] == "Alice"


def test_can_filter_by_roles(client):
    queried_response = client.get("/api/users?roles=1&roles=2")
    assert queried_response.status_code == 200
    assert len(queried_response.json()["data"]) == 2

    queried_response2 = client.get("/api/users?role=3&role=4")
    assert queried_response2.status_code == 200
    assert len(queried_response2.json()["data"]) == 10

    queried_response = client.get("/api/users?roles=1")
    assert queried_response.status_code == 200
    assert len(queried_response.json()["data"]) == 2

    queried_response = client.get("/api/users?sort=role")
    assert queried_response.status_code == 200
    assert len(queried_response.json()["data"]) == 10


def test_can_filter_by_user_active_field(client):
    queried_response = client.get("/api/users?active=true")
    assert queried_response.status_code == 200
    assert len(queried_response.json()["data"]) == 10

    queried_response2 = client.get("/api/users?active=false")
    assert queried_response2.status_code == 200
    assert len(queried_response2.json()["data"]) == 0

    queried_response_bad = client.get("/api/users?active=foo")
    assert queried_response_bad.status_code == 422
