import pytest
import requests


def pytest_addoption(parser):
    parser.addoption("--url", help="Параметр запроса url, по умолчанию https://ya.ru")

    parser.addoption(
        "--method",
        default="get",
        choices=["get", "post", "put", "patch", "delete"],
        help="method to execute",
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def request_method(request):
    return getattr(requests, request.config.getoption("--method"))


@pytest.fixture(scope="session")
def get_list_all_breeds_dogs():
    res = requests.get("https://dog.ceo/api/breeds/list/all")
    assert res.status_code == 200
    breed = list(res.json()["message"].keys())
    return breed
