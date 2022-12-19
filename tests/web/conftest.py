import string
from random import choice

import pytest
from selench import Selench


@pytest.fixture
def ui_driver():
    driver = Selench(wait=5)
    yield driver
    driver.quit()


@pytest.fixture
def person():
    generate_str = lambda x: "".join(
        [choice(choice([string.ascii_lowercase, string.ascii_uppercase, string.digits])) for _ in range(x)])

    _person = {
        "first_name": "David",
        "last_name": "Freitas",
        "address": "4436 Rhode Island Avenue",
        "city": "Washington",
        "state": "DC",
        "zipcode": 20036,
        "sex": "male",
        "phone": "202-331-1309",
        "email_address": "DavidMFreitas@armyspy.com",
        "ssn": "579-62-3889",
        "birthday": "September 2, 1941",
        "age": 80,
        "username": generate_str(8),
        "password": generate_str(12)}
    return _person
