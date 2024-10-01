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
    assert len(responses.json()["message"]) == pages


def test_dog_random_breed():
    breed = list(
        requests.get("https://dog.ceo/api/breeds/list/all").json()["message"].keys()
    )
    random_post_number = random.randint(0, len(breed))
    responses = requests.get(
        f"https://dog.ceo/api/breed/{breed[random_post_number]}/images/random"
    )
    assert breed[random_post_number] in responses.text


def test_dog_pages_more_50():
    responses = requests.get("https://dog.ceo/api/breeds/image/random/51")
    assert (len(responses.json()["message"])) == 50


@pytest.mark.parametrize("breed", ["corgi", "pembroke", "husky"])
def test_random_image_by_breed(breed):
    responses = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
    assert responses.status_code == 200
