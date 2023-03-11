import pytest


@pytest.fixture
def restful_booker_driver(driver):
    driver.get("https://automationintesting.online")
    driver.wait = 10
    return driver


@pytest.fixture
def logged_in_restful_booker(restful_booker_driver):
    restful_booker_driver.element('a[href*=admin]').click()
    restful_booker_driver.wait_for.elements_visibility('#username')
    restful_booker_driver.element('#username').send_keys('admin')
    restful_booker_driver.element('#password').send_keys('password')
    restful_booker_driver.element('#doLogin').click()
    return restful_booker_driver


def test_admin_panel_login(logged_in_restful_booker):
    assert logged_in_restful_booker.elements('//a[text()="Logout"]')


def test_create_room_with_valid_information(logged_in_restful_booker):
    name, type_, price, features = 102, "Double", 200, ["Refreshments", "Radio"]
    logged_in_restful_booker.element('#roomName').send_keys(name)
    logged_in_restful_booker.select_element(logged_in_restful_booker.element('#accessible')).select_by_value('true')
    logged_in_restful_booker.select_element(logged_in_restful_booker.element('#type')).select_by_value(type_)
    logged_in_restful_booker.element('#roomPrice').send_keys(price)

    for feature in features:
        logged_in_restful_booker.element(f'input[value={feature}]').click()

    logged_in_restful_booker.element('#createRoom').click()

    logged_in_restful_booker.get('https://automationintesting.online')

    result_type = logged_in_restful_booker.element(f'//img[contains(@alt,"room{name}")] /../.. //h3').text
    result_features = [i.text for i in
                       logged_in_restful_booker.elements(f'//img[contains(@alt,"room{name}")] /../.. //li')]
    assert result_type == type_
    assert all(i in " ".join(result_features) for i in features)


def test_create_room_with_incomplete_information(logged_in_restful_booker):
    logged_in_restful_booker.element('#roomName').send_keys(105)
    logged_in_restful_booker.select_element(logged_in_restful_booker.element('#accessible')).select_by_value('true')
    logged_in_restful_booker.select_element(logged_in_restful_booker.element('#type')).select_by_value('Double')
    logged_in_restful_booker.element('#createRoom').click()
    assert logged_in_restful_booker.elements('.alert-danger')


def test_cancel_room_booking(logged_in_restful_booker):
    name = 120
    logged_in_restful_booker.element('#roomName').send_keys(name)
    logged_in_restful_booker.select_element(logged_in_restful_booker.element('#accessible')).select_by_value('true')
    logged_in_restful_booker.select_element(logged_in_restful_booker.element('#type')).select_by_value('Family')
    logged_in_restful_booker.element('#roomPrice').send_keys(500)
    logged_in_restful_booker.element('#createRoom').click()
    logged_in_restful_booker.element(f'//p[@id="roomName{name}"] /../.. //span[contains(@class, "roomDelete")]').click()
    assert logged_in_restful_booker.wait_for.element_invisibility(f'#roomName{name}')


def test_branding_changes(logged_in_restful_booker, person):
    company = "Homer's Donuts"
    logo = "https://i.imgur.com/NMJtYCC.jpg"
    description = "Indulge in delicious donuts from the local bakery, nestled in the hills of Springfield."
    latitude = 38.905750
    longitude = 77.032010

    logged_in_restful_booker.element('#brandingLink').click()
    name_field = logged_in_restful_booker.wait_for.element_clickable('#name')
    name_field.clear()
    name_field.send_keys(company)
    logo_field = logged_in_restful_booker.element('#logoUrl')
    logo_field.clear()
    logo_field.send_keys(logo)
    description_field = logged_in_restful_booker.element('#description')
    description_field.clear()
    description_field.send_keys(description)
    latitude_field = logged_in_restful_booker.element('#latitude')
    latitude_field.clear()
    latitude_field.send_keys(latitude)
    longitude_field = logged_in_restful_booker.element('#longitude')
    longitude_field.clear()
    longitude_field.send_keys(longitude)
    contactName_field = logged_in_restful_booker.element('#contactName')
    contactName_field.clear()
    contactName_field.send_keys(person.first_name + " " + person.last_name)
    contactAddress_field = logged_in_restful_booker.element('#contactAddress')
    contactAddress_field.clear()
    contactAddress_field.send_keys(person.address)
    contactPhone_field = logged_in_restful_booker.element('#contactPhone')
    contactPhone_field.clear()
    contactPhone_field.send_keys(person.phone.replace("-", ""))
    contactEmail_field = logged_in_restful_booker.element('#contactEmail')
    contactEmail_field.clear()
    contactEmail_field.send_keys(person.email)

    logged_in_restful_booker.element('#updateBranding').click()
    logged_in_restful_booker.element('#frontPageLink').click()

    logged_in_restful_booker.wait_for.elements_visibility('img[class=hotel-logoUrl]')
    assert logged_in_restful_booker.element('.hotel-description p').text == description
    assert logged_in_restful_booker.element('//span[contains(@class, "fa-envelope")] //parent::p').text == person.email
