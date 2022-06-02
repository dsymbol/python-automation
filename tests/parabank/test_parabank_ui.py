import pytest

BASE_URI = "https://parabank.parasoft.com/parabank/index.htm"


@pytest.fixture
def driver(_driver):
    _driver.get(BASE_URI)
    _driver.wait = 10
    return _driver


def test_signup_signin(driver, person):
    # sign up

    driver.xpath_element('//a[contains(@href, "register.htm")]').click()
    driver.css_element('*[id="customer.firstName"]').send_keys(person["first_name"])
    driver.css_element('*[id="customer.lastName"]').send_keys(person["last_name"])
    driver.css_element('*[id="customer.address.street"]').send_keys(person["address"])
    driver.css_element('*[id="customer.address.city"]').send_keys(person["city"])
    driver.css_element('*[id="customer.address.state"]').send_keys(person["state"])
    driver.css_element('*[id="customer.address.zipCode"]').send_keys(person["zipcode"])
    driver.css_element('*[id="customer.phoneNumber"]').send_keys(person["phone"])
    driver.css_element('*[id="customer.ssn"]').send_keys(person["ssn"])
    driver.css_element('*[id="customer.username"]').send_keys(person["username"])
    driver.css_element('*[id="customer.password"]').send_keys(person["password"])
    driver.css_element('*[id="repeatedPassword"]').send_keys(person["password"])
    driver.xpath_element('//input[@value="Register"]').click()
    fullname = driver.xpath_element('//div[@id="leftPanel"] //p').text
    assert f'{person["first_name"]} {person["last_name"]}' in fullname

    # clear cookies before sign in
    driver.delete_cookies()
    driver.get(BASE_URI)

    # sign in
    driver.xpath_element('//form[contains(@action,"login.htm")] //input[@name="username"]').send_keys(
        person["username"])
    driver.xpath_element('//form[contains(@action,"login.htm")] //input[@name="password"]').send_keys(
        person["password"])
    driver.xpath_element('//form[contains(@action,"login.htm")] //input[@type="submit"]').submit()
    driver.wait_element_visibility(driver.css_element('div[id=rightPanel]'))
    account_id = driver.xpath_element('//a[contains(@href,"activity.htm")]').text
    assert account_id.isnumeric()
    balance = driver.xpath_element(
        '//a[contains(@href,"activity.htm")]  //parent::td //following-sibling::td').text
    assert "$" in balance


def test_about_us_page(driver):
    driver.xpath_element('//a[contains(@href,"about.htm")]').click()
    paragraphs = driver.xpath_elements('//div[@id="rightPanel"] /p')
    for paragraph in paragraphs:
        assert "Para" in paragraph.text


def test_services_page(driver):
    driver.xpath_element('//a[contains(@href,"services.htm")]').click()
    # Check that all service tables have content
    tables = len(driver.xpath_elements('//table'))
    for table in range(1, tables + 1):
        assert driver.xpath_elements(f'//table[{table}] //tr')


def test_products_buttons_redirect(driver):
    # First button
    driver.xpath_element('//div[@id="headerPanel"] //a[contains(@href,"products.js")]').click()
    assert driver.url == "https://www.parasoft.com/products/"
    driver.back()
    # Second button
    driver.xpath_element('//div[@id="footermainPanel"] //a[contains(@href,"products.js")]').click()
    assert driver.url == "https://www.parasoft.com/products/"


def test_locations_buttons_redirect(driver):
    # First button
    driver.xpath_element('//div[@id="headerPanel"] //a[contains(@href,"contacts.js")]').click()
    assert driver.url == "https://www.parasoft.com/solutions/"
    driver.back()
    # Second button
    driver.xpath_element('//div[@id="footermainPanel"] //a[contains(@href,"contacts.js")]').click()
    assert driver.url == "https://www.parasoft.com/solutions/"


def test_contact_us_form(driver, person):
    driver.xpath_element('//a[contains(@href,"contact.htm")]').click()
    driver.css_element("*[id=name]").send_keys(person["first_name"])
    driver.css_element("*[id=email]").send_keys(person["email_address"])
    driver.css_element("*[id=phone]").send_keys(person["phone"])
    driver.css_element("*[id=message]").send_keys("Testing contact us page :)")
    driver.xpath_element("//table //input[not(@id)]").click()
    finish_screen = driver.xpath_elements('//div[@id="rightPanel"] //p')
    assert person["first_name"] in finish_screen[0].text
    assert finish_screen[1].text == "A Customer Care Representative will be contacting you."


def test_admin_tools(driver):
    driver.xpath_element('//div[@id="headerPanel"] //a[contains(@href,"admin.htm")]').click()
    # db
    driver.xpath_element(
        '//form[@name="initializeDB" or contains(@action,"db.htm")] //button[@value="INIT"]').click()
    output = driver.xpath_element('//h1[@class="title"] /following-sibling::p').text
    assert "initial" in output.lower()
    driver.xpath_element(
        '//form[@name="initializeDB" or contains(@action,"db.htm")] //button[@value="CLEAN"]').click()
    output = driver.xpath_element('//h1[@class="title"] /following-sibling::p').text
    assert "clean" in output.lower()

    # jms service
    for i in range(2):
        service_toggle = driver.xpath_element(
            '//form[@name="toggleJms" or contains(@action,"jms.htm")] //input[not(@type="hidden")]')
        service_state_value = service_toggle.get_attribute("value")
        service_toggle.click()
        service_state = driver.xpath_element(
            '//form[@name="toggleJms" or contains(@action,"jms.htm")] //input[not('
            '@type="hidden")] /parent::* /preceding-sibling::td[text()]').text
        if service_state_value == "Shutdown":
            assert service_state.lower() == "stopped"
        elif service_state_value == "Startup":
            assert service_state.lower() == "running"

    # Data Access Mode, check that all radio buttons are clickable
    rbuttons = driver.xpath_elements('//form[@id="adminForm"] /table[1] //input')
    for rbutton in rbuttons:
        rbutton.click()
        assert rbutton.is_selected()

    # Test submit button
    submit_btn = driver.xpath_elements('//form[@id="adminForm"] //input')
    submit_btn[len(submit_btn) - 1].click()
    output = driver.xpath_element('//h1[@class="title"] /following-sibling::p').text
    assert output == "Settings saved successfully."
