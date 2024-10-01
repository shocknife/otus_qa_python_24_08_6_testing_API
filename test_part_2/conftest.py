import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru",
        help="Параметр запроса url, по умолчанию https://ya.ru",
    )

    parser.addoption(
        "--status_code", default=200, help="Параметр status_code, по умолчанию 200"
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def request_status_code(request):
    return request.config.getoption("--status_code")
