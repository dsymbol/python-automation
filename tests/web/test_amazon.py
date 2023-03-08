import pytest
from selenium.webdriver import Keys


@pytest.fixture
def driver(ui_driver):
    ui_driver.get("https://amazon.com")
    if not ui_driver.elements('#twotabsearchtextbox'):
        ui_driver.refresh()
    return ui_driver


products = ['raspberry pi', 'iphone', 'jbl flip']


@pytest.mark.parametrize('product', products)
def test_search_product(driver, product):
    driver.get("https://amazon.com")
    driver.element('input[name="field-keywords"]').send_keys(product, Keys.ENTER)
    titles = driver.elements('.s-card-container span.a-text-normal')
    relevant = [product in title.text.lower() for title in titles]
    assert relevant.count(True) >= len(relevant) * 0.5


def test_search_product_by_category(driver, product="raspberry"):
    driver.get("https://amazon.com")
    # all categories
    driver.element('input[name="field-keywords"]').send_keys(product, Keys.ENTER)
    titles = driver.elements('.s-card-container span.a-text-normal')
    relevant = ["raspberry pi" in title.text.lower() for title in titles]
    assert relevant.count(True) < len(relevant) * 0.8
    # category filtering
    select = driver.select_element(driver.element('select[class*=search]'))
    select.select_by_visible_text('Electronics')
    driver.element('input[name="field-keywords"]').send_keys(Keys.ENTER)
    titles = driver.elements('.s-card-container span.a-text-normal')
    relevant = ["raspberry pi" in title.text.lower() for title in titles]
    assert relevant.count(True) >= len(relevant) * 0.8


def test_search_autocomplete_suggestions(driver):
    search = driver.element('input[name="field-keywords"]')

    for product in products:
        search.send_keys(product)
        driver.wait_for.element_attribute_text_to_include('#issprefix', 'value', product)
        suggestions = [i.get_attribute('aria-label') for i in driver.elements('.s-suggestion-ellipsis-direction')]
        assert all(suggestion.startswith(product) for suggestion in suggestions)
        search.clear()


def test_search_filters(driver):
    driver.element('input[name="field-keywords"]').send_keys('cpu', Keys.ENTER)
    # # price filtering
    driver.elements('#priceRefinements ul li a')[1].click()
    prices = driver.elements('.a-price-whole')
    for price in prices:
        assert 25 <= int(price.text) <= 50
    # customer reviews
    driver.elements('#reviewsRefinements ul li a')[0].click()
    reviews = [i.get_attribute('class') for i in driver.elements('.s-card-container i[class*=a-icon-star]')]
    reviews = [''.join(filter(str.isdigit, s)) for s in reviews]
    for review in reviews:
        assert int(review) in [4, 45, 5]
