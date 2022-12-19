import pytest


@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}
