import pytest
from selenium.webdriver import Keys


@pytest.fixture
def parabank_driver(driver):
    driver.get("https://parabank.parasoft.com/parabank/index.htm")
    driver.wait = 10
    return driver


@pytest.fixture
def logged_in_parabank(parabank_driver, person):
    parabank_driver.element('[name="username"]').send_keys(person.username)
    parabank_driver.element('[name="password"]').send_keys(person.password, Keys.ENTER)
    return parabank_driver


def test_create_account(parabank_driver, person):
    parabank_driver.element('a[href*=register]').click()
    parabank_driver.element('[id="customer.firstName"]').send_keys(person.first_name)
    parabank_driver.element('[id="customer.lastName"]').send_keys(person.last_name)
    parabank_driver.element('[id="customer.address.street"]').send_keys(person.address)
    parabank_driver.element('[id="customer.address.city"]').send_keys(person.city)
    parabank_driver.element('[id="customer.address.state"]').send_keys(person.state)
    parabank_driver.element('[id="customer.address.zipCode"]').send_keys(person.zipcode)
    parabank_driver.element('[id="customer.phoneNumber"]').send_keys(person.phone)
    parabank_driver.element('[id="customer.ssn"]').send_keys(person.ssn)
    parabank_driver.element('[id="customer.username"]').send_keys(person.username)
    parabank_driver.element('[id="customer.password"]').send_keys(person.password)
    parabank_driver.element('[id="repeatedPassword"]').send_keys(person.password)
    parabank_driver.element('input[value=Register]').click()
    assert person.username in parabank_driver.element('#rightPanel h1').text
    assert 'created successfully' in parabank_driver.element('#rightPanel p').text.lower()
    assert parabank_driver.elements('a[href*=logout]')


def test_log_in_with_valid_credentials(logged_in_parabank, person):
    logged_in_parabank.wait_for.elements_visibility('#rightPanel')
    assert 'overview' in logged_in_parabank.url
    fullname = logged_in_parabank.element('#leftPanel p').text
    assert person.first_name + " " + person.last_name in fullname
    assert logged_in_parabank.elements('a[href*=logout]')


def test_login_persistence(logged_in_parabank, person):
    logged_in_parabank.element('a[href*=transfer]').click()
    assert logged_in_parabank.elements('a[href*=logout]')
    logged_in_parabank.element('img[src*=logo]').click()
    assert logged_in_parabank.elements('a[href*=logout]')


def test_log_in_with_invalid_credentials(parabank_driver, person):
    parabank_driver.element('[name="username"]').send_keys(person.username)
    parabank_driver.element('[name="password"]').send_keys('idontknow', Keys.ENTER)
    parabank_driver.wait_for.elements_visibility('#rightPanel')
    assert "error" in parabank_driver.element('#rightPanel h1').text.lower()
    assert not parabank_driver.elements('a[href*=logout]')
