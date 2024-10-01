import json
from jsonschema import validate
import pytest
import requests

base_url = "https://jsonplaceholder.typicode.com/"
headers = {"Content-Type": "application/json; charset=UTF-8"}


def test_get_all_posts():
    response = requests.get(f"{base_url}posts")
    assert response.status_code == 200
    assert response.json()[0]["id"] > 0


@pytest.mark.parametrize("id_num", [1, 3, 5])
def test_get_posts_by_id(id_num):
    response = requests.get(f"{base_url}posts/{id_num}")
    assert response.status_code == 200
    assert response.json()["id"] == id_num


@pytest.mark.parametrize(
    "data",
    [
        {"title": "Arny", "body": "Iron", "userId": 1},
        {"title": "Stalone", "body": "Steel", "userId": 2},
    ],
    ids=["Arny", "Stalone"],
)
def test_create_users_post(data):
    response = requests.post(f"{base_url}posts", json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json()["id"] == 101


def test_update_put():
    data = {"title": "Change  title", "body": "change body", "userId": 1, "id": 1}
    response = requests.put(f"{base_url}posts/1", json.dumps(data), headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Change  title"
    assert response.json()["body"] == "change body"
    assert response.json()["id"] == 1


def test_validate_schema_post():
    res = requests.get(f"{base_url}/comments?postId=1")
    schema = {
        "postId": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "body": {"type": "string"},
    }

    validate(instance=res.json(), schema=schema)
