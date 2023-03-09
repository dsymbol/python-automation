import pytest
from selenium.webdriver import Keys


@pytest.fixture
def driver(ui_driver):
    ui_driver.get("https://parabank.parasoft.com/parabank/index.htm")
    ui_driver.wait = 10
    return ui_driver


def test_create_account(driver, person):
    driver.element('a[href*=register]').click()
    driver.element('[id="customer.firstName"]').send_keys(person.first_name)
    driver.element('[id="customer.lastName"]').send_keys(person.last_name)
    driver.element('[id="customer.address.street"]').send_keys(person.address)
    driver.element('[id="customer.address.city"]').send_keys(person.city)
    driver.element('[id="customer.address.state"]').send_keys(person.state)
    driver.element('[id="customer.address.zipCode"]').send_keys(person.zipcode)
    driver.element('[id="customer.phoneNumber"]').send_keys(person.phone)
    driver.element('[id="customer.ssn"]').send_keys(person.ssn)
    driver.element('[id="customer.username"]').send_keys(person.username)
    driver.element('[id="customer.password"]').send_keys(person.password)
    driver.element('[id="repeatedPassword"]').send_keys(person.password)
    driver.element('input[value=Register]').click()
    assert person.username in driver.element('#rightPanel h1').text
    assert 'created successfully' in driver.element('#rightPanel p').text.lower()
    assert driver.elements('a[href*=logout]')


def test_log_in_with_valid_credentials(driver, person):
    driver.element('[name="username"]').send_keys(person.username)
    driver.element('[name="password"]').send_keys(person.password, Keys.ENTER)
    driver.wait_for.elements_visibility('#rightPanel')
    assert 'overview' in driver.url
    fullname = driver.element('#leftPanel p').text
    assert person.first_name + " " + person.last_name in fullname
    assert driver.elements('a[href*=logout]')


def test_login_persistence(driver, person):
    test_log_in_with_valid_credentials(driver, person)
    driver.element('a[href*=transfer]').click()
    assert driver.elements('a[href*=logout]')
    driver.element('img[src*=logo]').click()
    assert driver.elements('a[href*=logout]')


def test_log_in_with_invalid_credentials(driver, person):
    driver.element('[name="username"]').send_keys(person.username)
    driver.element('[name="password"]').send_keys('idontknow', Keys.ENTER)
    driver.wait_for.elements_visibility('#rightPanel')
    assert "error" in driver.element('#rightPanel h1').text.lower()
    assert not driver.elements('a[href*=logout]')
