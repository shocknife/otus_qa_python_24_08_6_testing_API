import requests
import pytest

base_url = "https://api.openbrewerydb.org/v1/breweries"


@pytest.mark.parametrize(
    "brewery_id, country_brewery",
    [
        ("5128df48-79fc-4f0f-8b52-d06be54d0cec", "United States"),
        ("ad5ab314-fdc4-4f12-a3d5-6fbb4f8ed7a3", "Scotland"),
        ("745272b9-5d04-4468-b1f7-e76a75c22de9", "England"),
    ],
    ids=["United States", "Scotland", "England"],
)
def test_get_single_brewery(brewery_id, country_brewery):
    response = requests.get(f"{base_url}/{brewery_id}")
    assert response.status_code == 200
    assert response.json()["id"] == brewery_id
    assert response.json()["country"] == country_brewery


@pytest.mark.parametrize("city", ["Norman", "Bend", "Denver"])
def test_get_breweries_by_city(city):
    response = requests.get(f"{base_url}?by_city={city}", params={"per_page": 1})
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["city"] == city


@pytest.mark.parametrize("state", ["Argyll", "Idaho"])
def test_get_breweries_by_state(state):
    response = requests.get(f"{base_url}?by_state={state}")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.parametrize("query", ["Beerfoot", "Atlanti"])
def test_search_breweries(query):
    response = requests.get(f"{base_url}/search?query={query}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert query in response.text


@pytest.mark.parametrize("pages", [1, 2, 3])
def test_dog_pages(pages):
    responses = requests.get(f"{base_url}/random", params={"size": pages})
    assert len(responses.json()) == pages
