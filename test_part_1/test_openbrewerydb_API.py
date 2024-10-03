import requests
import pytest

base_url = "https://api.openbrewerydb.org/v1/breweries"


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
    assert response.json()[0]["state"] == state


@pytest.mark.parametrize("query", ["Beerfoot", "Atlanti"])
def test_search_breweries(query):
    response = requests.get(f"{base_url}/search?query={query}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert query in response.text


@pytest.mark.parametrize("pages", [1, 2, 3])
def test_dog_pages(pages):
    responses = requests.get(f"{base_url}/random", params={"size": pages})
    assert responses.status_code == 200
    assert len(responses.json()) == pages


def test_get_single_brewery():
    res_random = requests.get(f"{base_url}/random")
    assert res_random.status_code == 200
    brewery_id = res_random.json()[0]["id"]
    country_brewery = res_random.json()[0]["country"]
    response = requests.get(f"{base_url}/{brewery_id}")
    assert response.status_code == 200
    assert response.json()["id"] == brewery_id
    assert response.json()["country"] == country_brewery
