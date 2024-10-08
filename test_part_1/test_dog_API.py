import random
import pytest
import requests
from jsonschema import validate


def test_dog_api_json_schema():
    res = requests.get("https://dog.ceo/api/breeds/image/random/")
    schema = {"message": {"type": "string"}, "status": {"type": "string"}}
    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize(
    "url, text, status_code",
    [
        ("https://dog.ceo/api/breeds/list/stringa", "error", 404),
        ("https://dog.ceo/api/breeds/image/random", "message", 200),
    ],
    ids=["Bad address", "Correct address"],
)
def test_dog_verify_address(url, text, status_code):
    responses = requests.get(url)
    assert responses.status_code == status_code
    assert text in responses.text


@pytest.mark.parametrize("pages", [1, 2, 3])
def test_dog_pages(pages):
    responses = requests.get(f"https://dog.ceo/api/breeds/image/random/{pages}")
    assert responses.status_code == 200
    assert len(responses.json()["message"]) == pages


@pytest.mark.parametrize("pages", [50, 51, 100])
def test_dog_pages_more_50(pages):
    responses = requests.get(f"https://dog.ceo/api/breeds/image/random/{pages}")
    assert responses.status_code == 200
    assert (len(responses.json()["message"])) == 50


@pytest.mark.parametrize("breed", ["corgi", "pembroke", "husky"])
def test_random_image_by_breed(breed):
    responses = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
    assert responses.status_code == 200
    assert responses.json()["status"] == "success"
    assert breed in responses.text


def get_list_all_breeds_dogs():
    res = requests.get("https://dog.ceo/api/breeds/list/all")
    assert res.status_code == 200
    breeds = list(res.json()["message"].keys())
    return breeds

#Запускает генератор по списку полученных пород собак
def breed_generator(breeds, num_breeds=10):
    random_breeds = random.sample(breeds, num_breeds)
    for breed in random_breeds:
        yield breed

#использует генератор в параметрах. Через фикстуру запустить не получается.
@pytest.mark.parametrize("breed", breed_generator(get_list_all_breeds_dogs(), 5))
def test_dog_random_breed(breed):
    responses = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
    assert responses.status_code == 200
    assert breed in responses.text
