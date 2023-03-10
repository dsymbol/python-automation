import pytest


@pytest.fixture
def driver(ui_driver):
    ui_driver.get("https://automationintesting.online")
    ui_driver.wait = 10
    return ui_driver


def test_admin_panel_login(driver):
    driver.element('a[href*=admin]').click()
    driver.wait_for.elements_visibility('#username')
    driver.element('#username').send_keys('admin')
    driver.element('#password').send_keys('password')
    driver.element('#doLogin').click()
    assert driver.elements('//a[text()="Logout"]')


def test_create_room_with_valid_information(driver):
    test_admin_panel_login(driver)

    name, type_, price, features = 102, "Double", 200, ["Refreshments", "Radio"]
    driver.element('#roomName').send_keys(name)
    driver.select_element(driver.element('#accessible')).select_by_value('true')
    driver.select_element(driver.element('#type')).select_by_value(type_)
    driver.element('#roomPrice').send_keys(price)

    for feature in features:
        driver.element(f'input[value={feature}]').click()

    driver.element('#createRoom').click()

    driver.get('https://automationintesting.online')

    result_type = driver.element(f'//img[contains(@alt,"room{name}")] /../.. //h3').text
    result_features = [i.text for i in driver.elements(f'//img[contains(@alt,"room{name}")] /../.. //li')]
    assert result_type == type_
    assert all(i in " ".join(result_features) for i in features)


def test_create_room_with_incomplete_information(driver):
    test_admin_panel_login(driver)
    driver.element('#roomName').send_keys(105)
    driver.select_element(driver.element('#accessible')).select_by_value('true')
    driver.select_element(driver.element('#type')).select_by_value('Double')
    driver.element('#createRoom').click()
    assert driver.elements('.alert-danger')


def test_cancel_room_booking(driver):
    test_admin_panel_login(driver)
    name = 120
    driver.element('#roomName').send_keys(name)
    driver.select_element(driver.element('#accessible')).select_by_value('true')
    driver.select_element(driver.element('#type')).select_by_value('Family')
    driver.element('#roomPrice').send_keys(500)
    driver.element('#createRoom').click()
    driver.element(f'//p[@id="roomName{name}"] /../.. //span[contains(@class, "roomDelete")]').click()
    assert driver.wait_for.element_invisibility(f'#roomName{name}')


def test_branding_changes(driver, person):
    test_admin_panel_login(driver)
    company = "Homer's Donuts"
    logo = "https://i.imgur.com/NMJtYCC.jpg"
    description = "Indulge in delicious donuts from the local bakery, nestled in the hills of Springfield."
    latitude = 38.905750
    longitude = 77.032010

    driver.element('#brandingLink').click()
    name_field = driver.wait_for.element_clickable('#name')
    name_field.clear()
    name_field.send_keys(company)
    logo_field = driver.element('#logoUrl')
    logo_field.clear()
    logo_field.send_keys(logo)
    description_field = driver.element('#description')
    description_field.clear()
    description_field.send_keys(description)
    latitude_field = driver.element('#latitude')
    latitude_field.clear()
    latitude_field.send_keys(latitude)
    longitude_field = driver.element('#longitude')
    longitude_field.clear()
    longitude_field.send_keys(longitude)
    contactName_field = driver.element('#contactName')
    contactName_field.clear()
    contactName_field.send_keys(person.first_name + " " + person.last_name)
    contactAddress_field = driver.element('#contactAddress')
    contactAddress_field.clear()
    contactAddress_field.send_keys(person.address)
    contactPhone_field = driver.element('#contactPhone')
    contactPhone_field.clear()
    contactPhone_field.send_keys(person.phone.replace("-", ""))
    contactEmail_field = driver.element('#contactEmail')
    contactEmail_field.clear()
    contactEmail_field.send_keys(person.email)

    driver.element('#updateBranding').click()
    driver.element('#frontPageLink').click()

    driver.wait_for.elements_visibility('img[class=hotel-logoUrl]')
    assert driver.element('.hotel-description p').text == description
    assert driver.element('//span[contains(@class, "fa-envelope")] //parent::p').text == person.email
