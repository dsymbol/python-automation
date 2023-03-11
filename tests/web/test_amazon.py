import pytest
from selenium.webdriver import Keys


@pytest.fixture
def amazon_driver(driver):
    driver.get("https://amazon.com")
    if not driver.elements('#twotabsearchtextbox'):
        driver.refresh()
    return driver


products = ['raspberry pi', 'iphone', 'jbl flip']


@pytest.mark.parametrize('product', products)
def test_search_product(amazon_driver, product):
    amazon_driver.get("https://amazon.com")
    amazon_driver.element('input[name="field-keywords"]').send_keys(product, Keys.ENTER)
    titles = amazon_driver.elements('.s-card-container span.a-text-normal')
    relevant = [product in title.text.lower() for title in titles]
    assert relevant.count(True) >= len(relevant) * 0.5


def test_search_product_by_category(amazon_driver, product="raspberry"):
    amazon_driver.get("https://amazon.com")
    # all categories
    amazon_driver.element('input[name="field-keywords"]').send_keys(product, Keys.ENTER)
    titles = amazon_driver.elements('.s-card-container span.a-text-normal')
    relevant = ["raspberry pi" in title.text.lower() for title in titles]
    assert relevant.count(True) < len(relevant) * 0.8
    # category filtering
    select = amazon_driver.select_element('select[class*=search]')
    select.select_by_visible_text('Electronics')
    amazon_driver.element('input[name="field-keywords"]').send_keys(Keys.ENTER)
    titles = amazon_driver.elements('.s-card-container span.a-text-normal')
    relevant = ["raspberry pi" in title.text.lower() for title in titles]
    assert relevant.count(True) >= len(relevant) * 0.8


def test_search_autocomplete_suggestions(amazon_driver):
    search = amazon_driver.element('input[name="field-keywords"]')

    for product in products:
        search.send_keys(product)
        amazon_driver.wait_for.element_attribute_text_to_include('#issprefix', 'value', product)
        suggestions = [i.get_attribute('aria-label') for i in amazon_driver.elements('.s-suggestion-ellipsis-direction')]
        assert all(suggestion.startswith(product) for suggestion in suggestions)
        search.clear()


def test_search_filters(amazon_driver):
    amazon_driver.element('input[name="field-keywords"]').send_keys('cpu', Keys.ENTER)
    # price filtering
    amazon_driver.elements('#priceRefinements ul li a')[1].click()
    prices = amazon_driver.elements('.a-price-whole')
    for price in prices:
        assert 25 <= int(price.text) <= 50
    # customer reviews
    amazon_driver.elements('#reviewsRefinements ul li a')[0].click()
    reviews = [i.get_attribute('class') for i in amazon_driver.elements('.s-card-container i[class*=a-icon-star]')]
    reviews = [''.join(filter(str.isdigit, s)) for s in reviews]
    for review in reviews:
        assert int(review) in [4, 45, 5]


ms_products = [('Sunglases', 'sunglasses'), ('Furnitue', 'furniture'), ('Aplle', 'apple')]


@pytest.mark.parametrize('incorrect, correct', ms_products)
def test_search_for_misspelled_product(amazon_driver, incorrect, correct):
    amazon_driver.element('input[name="field-keywords"]').send_keys(incorrect, Keys.ENTER)
    titles = [i.text for i in amazon_driver.elements('.s-card-container span.a-text-normal')]
    assert "\n".join(titles).lower().count(correct) > 10


def test_search_out_of_stock_product(amazon_driver):
    amazon_driver.element('input[name="field-keywords"]').send_keys('airtag', Keys.ENTER)
    assert not amazon_driver.elements('[data-cel-widget="search_result_1"] .a-price-whole')
