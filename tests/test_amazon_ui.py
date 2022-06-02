import pytest
from selenium.webdriver import Keys

BASE_URI = "https://www.amazon.com/"


@pytest.fixture
def driver(_driver):
    _driver.get(BASE_URI)
    if _driver.xpath_elements('//input[@data-action-type="DISMISS"]'):
        _driver.xpath_element('//input[@data-action-type="DISMISS"]').click()
    while True:
        if _driver.css_elements('*[id=twotabsearchtextbox]'):
            break
        _driver.refresh()
    return _driver


phrases = [("ram"), ("Raspberry Pi"), ("CPU")]


@pytest.mark.parametrize('phrase', phrases)
def test_search_query(driver, phrase):
    # Search element
    driver.css_element("*[id=twotabsearchtextbox]").send_keys(phrase)
    # Submit search element
    driver.css_element("*[id=nav-search-submit-button]").submit()
    prices = driver.xpath_elements(
        '//div[contains(@class, "s-result-item s-asin") and not(contains(@class, '
        '"AdHolder"))] //span[@class="a-price-whole"]')
    for price in prices:
        assert int(price.text) > 0

    assert phrase in driver.title
    search_query = driver.xpath_element('//span[@class="a-color-state a-text-bold"]').text
    assert search_query == f'"{phrase}"'


def test_today_deals(driver):
    # Today's deals button on frontpage
    driver.xpath_element(
        '//div[@id="nav-xshop"] /a[@data-csa-c-slot-id="nav_cs_0"]').click()
    assert "goldbox" in driver.url
    # The deals in percent or dollars off (red box)
    deals = driver.xpath_elements(
        '//div[@class="BadgeAutomated-module__badgeOneLineContainer_yYupgq1lKxb5h3bfDqA-B"] '
        '//div['
        '@class="BadgeAutomatedLabel-module__badgeAutomatedLabel_2Teem9LTaUlj6gBh5R45wd"]')
    for deal in deals:
        assert "$" or "%" in deal.text
    assert "deals" in driver.title.lower()


def test_invalid_email_signin(driver):
    driver.css_element("*[id=nav-link-accountList]").click()
    driver.css_element("*[id=ap_email]").send_keys("test2022auth@email.com")
    driver.css_element("*[id=continue-announce]").submit()
    error_message = driver.css_element("*[class=a-alert-heading]")
    assert error_message.text == "There was a problem"


def test_customer_service(driver):
    driver.xpath_element(
        '//div[@id="nav-xshop"] /a[@data-csa-c-slot-id="nav_cs_1"]').click()
    driver.xpath_element('//input[@id="helpsearch" or @id="hubHelpSearchInput"]').send_keys("refund", Keys.ENTER)
    answer = driver.xpath_element('//div[contains(@class,"answer-box-t1")] //h2')
    assert "refund" in answer.text.lower()


def test_cart(driver):
    # Search element
    driver.css_element("*[id=twotabsearchtextbox]").send_keys("gpu")
    # Submit search element
    driver.css_element("*[id=nav-search-submit-button]").submit()
    product = driver.xpath_element('(//div[contains(@class, "s-result-item s-asin") and not(contains(@class, '
                                   '"AdHolder"))] '
                                   '//span[contains(@class,"a-size-medium")])[1]')
    p_text = product.text
    product.click()
    driver.css_element('*[id=add-to-cart-button]').click()
    driver.xpath_element('//span[@id="sw-gtc"] /span').click()
    cart_product = driver.css_element("*[class=a-truncate-cut]")
    # Compare first 3 words of product added to cart and product in cart
    assert p_text.split(" ")[:3] == cart_product.text.split(" ")[:3]
