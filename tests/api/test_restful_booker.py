import pytest
import requests

BASE_URI = "https://restful-booker.herokuapp.com"


@pytest.fixture
def token_headers(headers):
    response = requests.post(f"{BASE_URI}/auth", headers=headers, json={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    token = response.json()["token"]
    headers['Cookie'] = f"token={token}"
    return headers


def test_api_health(headers):
    response = requests.get(f'{BASE_URI}/ping', headers=headers)
    assert response.status_code == 201


def test_get_booking_ids(headers):
    response = requests.get(f'{BASE_URI}/booking', headers=headers)
    assert response.status_code == 200
    for i in response.json():
        assert int(i["bookingid"])


people = [("Bart", "PS5"), ("Lisa", "Books"), ("Homer", "Donuts")]


@pytest.mark.parametrize('name, additional', people)
def test_create_booking(headers, name, additional):
    # Book a room
    book_room = requests.post(f'{BASE_URI}/booking', headers=headers, json={
        "firstname": name,
        "lastname": "Simpson",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2022-01-01",
            "checkout": "2022-02-01"
        },
        "additionalneeds": additional
    })
    assert book_room.status_code == 200
    assert book_room.json()["booking"]["additionalneeds"] == additional


@pytest.mark.parametrize('name, additional', people)
def test_get_booking_details_by_name(headers, name, additional):
    room_by_name = requests.get(f'{BASE_URI}/booking?firstname={name}&lastname=Simpson', headers=headers).json()[0][
        "bookingid"]
    assert int(room_by_name)
    room_details_by_id = requests.get(f'{BASE_URI}/booking/{room_by_name}', headers=headers).json()
    assert room_details_by_id['additionalneeds'] == additional


def test_update_booking(token_headers, headers):
    new_need = "food"
    room_by_name = requests.get(f'{BASE_URI}/booking?firstname=Homer&lastname=Simpson', headers=headers).json()[0][
        "bookingid"]
    update_room = requests.patch(f'{BASE_URI}/booking/{room_by_name}', headers=token_headers,
                                 json={"additionalneeds": new_need})
    assert update_room.status_code == 200
    assert update_room.json()['additionalneeds'] == new_need


def test_delete_booking(token_headers, headers):
    room_by_name = requests.get(f'{BASE_URI}/booking?firstname=Homer&lastname=Simpson', headers=headers).json()[0][
        "bookingid"]
    delete_room = requests.delete(f'{BASE_URI}/booking/{room_by_name}', headers=token_headers)
    assert delete_room.status_code == 201
