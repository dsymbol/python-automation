import pytest
from selench import Selench

from utils.helpers import random_person


@pytest.fixture
def ui_driver():
    driver = Selench(wait=5)
    yield driver
    driver.quit()


@pytest.fixture
def person():
    return random_person()


@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}
