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
