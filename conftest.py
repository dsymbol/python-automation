import pytest
from selench import Selench

from utils.data_generator import person_generator


@pytest.fixture
def _driver():
    driver = Selench(wait=5)
    yield driver
    driver.quit()


@pytest.fixture
def person():
    return person_generator()


@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}
