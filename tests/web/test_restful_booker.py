def test_admin_panel_login(driver):
    driver.get("https://automationintesting.online")
    driver.element('a[href*=admin]').click()
    driver.expect.element_to_be_visible('#username')
    driver.element('#username').send_keys('admin')
    driver.element('#password').send_keys('password')
    driver.element('#doLogin').click()
    assert driver.elements('//a[text()="Logout"]')


def test_create_room_with_valid_information(driver):
    driver.get("https://automationintesting.online")
    driver.element('a[href*=admin]').click()
    driver.expect.element_to_be_visible('#username')
    driver.element('#username').send_keys('admin')
    driver.element('#password').send_keys('password')
    driver.element('#doLogin').click()
    name, type_, price, features = 102, "Double", 200, ["Refreshments", "Radio"]
    driver.element('#roomName').send_keys(name)
    driver.element('#accessible').select_by_value('true')
    driver.element('#type').select_by_value(type_)
    driver.element('#roomPrice').send_keys(price)

    for feature in features:
        driver.element(f'input[value={feature}]').click()

    driver.element('#createRoom').click()
    driver.get('https://automationintesting.online')

    room = None
    for element in driver.elements('.hotel-room-info'):
        if element.is_displayed() and element.elements('.hotel-room-info [alt*=room102]'):
            room = element

    result_type = room.element("h3").text
    result_features = [i.text for i in room.elements(f'li')]
    assert result_type == type_
    assert all(i in " ".join(result_features) for i in features)


def test_create_room_with_incomplete_information(driver):
    driver.get("https://automationintesting.online")
    driver.element('a[href*=admin]').click()
    driver.expect.element_to_be_visible('#username')
    driver.element('#username').send_keys('admin')
    driver.element('#password').send_keys('password')
    driver.element('#doLogin').click()
    driver.element('#roomName').send_keys(105)
    driver.element('#accessible').select_by_value('true')
    driver.element('#type').select_by_value('Double')
    driver.element('#createRoom').click()
    assert driver.elements('.alert-danger')
