import pytest


@pytest.fixture
def saucedemo_page(page):
    page.goto('https://www.saucedemo.com')
    return page


@pytest.fixture
def logged_in_saucedemo(saucedemo_page):
    saucedemo_page.locator('[placeholder="Username"]').type('standard_user')
    saucedemo_page.locator('[placeholder="Password"]').type('secret_sauce')
    saucedemo_page.locator('#login-button').click()
    return saucedemo_page


def test_log_in_with_valid_credentials(logged_in_saucedemo):
    assert logged_in_saucedemo.locator('a[class*=shopping]').all()
    assert logged_in_saucedemo.locator('//button[text()="Add to cart"]').all()


def test_login_with_invalid_credentials(saucedemo_page):
    saucedemo_page.locator('[placeholder="Username"]').type('invalid_user')
    saucedemo_page.locator('[placeholder="Password"]').type('no_sauce')
    saucedemo_page.locator('#login-button').click()
    assert saucedemo_page.locator('[data-test="error"]').all()


def test_add_to_cart(logged_in_saucedemo):
    item = logged_in_saucedemo.locator('.inventory_item_name').nth(0).inner_text()
    logged_in_saucedemo.locator('#add-to-cart-sauce-labs-backpack').click()
    logged_in_saucedemo.locator('a[class*=shopping]').click()
    assert logged_in_saucedemo.locator('.inventory_item_name').nth(0).inner_text() == item


def test_add_to_cart_from_product_page(logged_in_saucedemo):
    logged_in_saucedemo.locator('.inventory_item_name').nth(0).click()
    item = logged_in_saucedemo.locator('.inventory_details_name').inner_text()
    logged_in_saucedemo.locator('#add-to-cart-sauce-labs-backpack').click()
    logged_in_saucedemo.locator('a[class*=shopping]').click()
    assert logged_in_saucedemo.locator('.inventory_item_name').nth(0).inner_text() == item


def test_remove_from_cart(logged_in_saucedemo):
    logged_in_saucedemo.locator('#add-to-cart-sauce-labs-backpack').click()
    logged_in_saucedemo.locator('a[class*=shopping]').click()
    logged_in_saucedemo.locator('#remove-sauce-labs-backpack').click()
    assert not logged_in_saucedemo.locator('.cart_item').all()


def test_product_sorting(logged_in_saucedemo):
    sel = logged_in_saucedemo.locator('select.product_sort_container')
    # A to Z
    sel.select_option('az')
    sorted_titles = [i.inner_text() for i in logged_in_saucedemo.locator('.inventory_item_name').all()]
    assert sorted(sorted_titles) == sorted_titles
    # Z to A
    sel.select_option('za')
    reverse_sorted_titles = [i.inner_text() for i in logged_in_saucedemo.locator('.inventory_item_name').all()]
    assert sorted(reverse_sorted_titles, reverse=True) == reverse_sorted_titles
    # low to high
    sel.select_option('lohi')
    sorted_prices = [float(i.inner_text().replace('$', '')) for i in logged_in_saucedemo.locator('.inventory_item_price').all()]
    assert sorted(sorted_prices) == sorted_prices
    # high to low
    sel.select_option('hilo')
    reverse_sorted_prices = [float(i.inner_text().replace('$', '')) for i in
                             logged_in_saucedemo.locator('.inventory_item_price').all()]
    assert sorted(reverse_sorted_prices, reverse=True) == reverse_sorted_prices


def test_checkout_cart(logged_in_saucedemo):
    logged_in_saucedemo.locator('#add-to-cart-sauce-labs-backpack').click()
    logged_in_saucedemo.locator('a[class*=shopping]').click()
    logged_in_saucedemo.locator('#checkout').click()
    logged_in_saucedemo.locator('#first-name').type('Homer')
    logged_in_saucedemo.locator('#last-name').type('Simpson')
    logged_in_saucedemo.locator('#postal-code').type('00000')
    logged_in_saucedemo.locator('#continue').click()
    logged_in_saucedemo.locator('#finish').click()
    assert "complete" in logged_in_saucedemo.locator('.title').inner_text().lower()
    assert logged_in_saucedemo.locator('.complete-header').all()
    assert logged_in_saucedemo.locator('.complete-text').all()
