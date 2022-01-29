import time
from typing import List

import requests
from requests import Response

SHORT_URLS: List[str] = []


def test_create_short_url(endpoint: str):
    response: Response = requests.put(f"{endpoint}/slug", json={"long_url": "https://example.com"})
    assert response.status_code == 200
    assert "slug" in response.json()
    SHORT_URLS.append(response.json()['short_url'])


def test_create_short_url_with_expiry(endpoint: str):
    response: Response = requests.put(f"{endpoint}/slug",
                                      json={"long_url": "https://example.com", "expires": {"days": 7}})
    assert response.status_code == 200
    assert "slug" in response.json()
    SHORT_URLS.append(response.json()['short_url'])


def test_create_short_url_with_no_long_url(endpoint: str):
    response: Response = requests.put(f"{endpoint}/slug", json={"long_url": None})
    assert response.status_code == 400


def test_create_short_url_with_malformed_expiry(endpoint: str):
    # Bad Unit
    response: Response = requests.put(f"{endpoint}/slug", json={"long_url": "https://example.com",
                                                                "expires": {"decades": 7}})
    assert response.status_code == 400

    # Bad Value - Int
    response: Response = requests.put(f"{endpoint}/slug", json={"long_url": "https://example.com",
                                                                "expires": {"days": "W"}})
    assert response.status_code == 400

    # Bad Value - Range
    response: Response = requests.put(f"{endpoint}/slug", json={"long_url": "https://example.com",
                                                                "expires": {"days": -7}})
    assert response.status_code == 400


def test_expand_url():
    response: Response = requests.get("http://" + SHORT_URLS[1], allow_redirects=False)
    assert response.is_redirect
    assert response.headers.get('location') == "https://example.com"


def test_expand_url_with_non_existent_slug(endpoint: str):
    response: Response = requests.get(f"{endpoint}/NXSLUG", allow_redirects=False)
    assert response.status_code == 404


def test_describe(endpoint: str):
    test_slug = SHORT_URLS[1].split('/')[-1]
    response: Response = requests.get(f"{endpoint}/slugs/{test_slug}")
    assert response.status_code == 200

    json = response.json()

    assert json['slug'] == test_slug
    assert json['long_url'] == "https://example.com"
    assert json['expires']
    assert not json['expired']
    assert json['stats'] == {"last_day": 1, "last_week": 1, "all_time": 1}


def test_describe_non_existent_slug(endpoint: str):
    response: Response = requests.get(f"{endpoint}/slugs/NXSLUG")
    assert response.status_code == 404


def text_expiring_url(endpoint: str):
    create_response: Response = requests.put(f"{endpoint}/slug",
                                             json={"long_url": "https://example.com", "expires": {"seconds": 10}})
    assert create_response.status_code == 200
    SHORT_URLS.append(create_response.json()['short_url'])

    short_url = f"http://{create_response.json()['short_url']}"
    first_get_response: Response = requests.get(short_url, allow_redirects=False)
    assert first_get_response.is_redirect

    time.sleep(11)

    second_get_response: Response = requests.get(short_url, allow_redirects=False)
    assert second_get_response.status_code == 410


def test_delete_short_url(endpoint: str):
    delete_response: Response = requests.delete(f"{endpoint}/slugs/{SHORT_URLS[0].split('/')[-1]}")
    assert delete_response.status_code == 200

    get_response: Response = requests.get("http://" + SHORT_URLS[0], allow_redirects=False)
    assert get_response.status_code == 404


def test_delete_non_existent_short_url(endpoint: str):
    delete_response: Response = requests.delete(f"{endpoint}/slugs/NXSLUG")
    assert delete_response.status_code == 404
