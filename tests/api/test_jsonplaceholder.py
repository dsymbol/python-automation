"""
Important: resource will not be really updated on the server but it will be faked as if.
"""
from random import randint

import pytest
import requests

BASE_URI = "https://jsonplaceholder.typicode.com"


def test_get_all_posts(headers):
    response = requests.get(f'{BASE_URI}/posts', headers=headers)
    assert response.status_code == 200
    keys = ["userId", "id", "title", "body"]
    for post in response.json():
        assert all(i in post.keys() for i in keys)


def test_get_single_post(headers):
    random_post = randint(1, 100)
    response = requests.get(f'{BASE_URI}/posts/{random_post}', headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == random_post


post_products = [(dict(title="apple", body="red", userId=4), 201), (dict(title="apple", userId=5), 201)]


@pytest.mark.parametrize('body, code', post_products)
def test_create_post(headers, body, code):
    response = requests.post(f'{BASE_URI}/posts', json=body, headers=headers)
    assert response.status_code == code


update_products = [(1, 200), (150, 500)]


@pytest.mark.parametrize('post, code', update_products)
def test_update_post(headers, post, code):
    response = requests.put(f'{BASE_URI}/posts/{post}', json=dict(title="apple", body="red", userId=4),
                            headers=headers)
    assert response.status_code == code


def test_partially_update_post(headers):
    response = requests.patch(f'{BASE_URI}/posts/50', json=dict(title="apple"),
                              headers=headers)
    assert response.status_code == 200


def test_delete_post(headers):
    response = requests.delete(f'{BASE_URI}/posts/50', headers=headers)
    assert response.status_code == 200


filter_nested_products = [(1, 1), (2, 2), (3, 3)]


@pytest.mark.parametrize('id, expected_id', filter_nested_products)
def test_filtering_nested_resources(headers, id, expected_id):
    filtering = requests.get(f"{BASE_URI}/posts?userId={id}", headers=headers)
    nested = requests.get(f"{BASE_URI}/posts/{id}/comments", headers=headers)
    assert nested.status_code == 200 and filtering.status_code == 200
    for i, j in zip(filtering.json(), nested.json()):
        assert i["userId"] == expected_id and j["postId"] == expected_id
