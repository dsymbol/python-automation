from dataclasses import dataclass

import pytest
from playwright.sync_api import sync_playwright
from selench import Selench


@pytest.fixture
def driver():
    driver = Selench(wait=5)
    yield driver
    driver.quit()


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture
def person():
    return Person("homer123")


@dataclass
class Person:
    username: str
    first_name: str = "Homer"
    last_name: str = "Simpson"
    address: str = "742 Evergreen Terrace"
    city: str = "Springfield"
    state: str = "Unknown"
    zipcode: int = 00000
    sex: str = "Male"
    phone: str = "555-555-5555"
    email: str = "homer@simpson.com"
    ssn: str = "123-45-6789"
    birthday: str = "May 12, 1956"
    age: int = 66
    password: str = "doh123"
