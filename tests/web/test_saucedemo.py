import pytest


@pytest.fixture
def page(ui_page):
    ui_page.goto('https://www.saucedemo.com')
    ui_page.locator('[placeholder="Username"]').type('standard_user')
    ui_page.locator('[placeholder="Password"]').type('secret_sauce')
    ui_page.locator('#login-button').click()
    return ui_page


def test_log_in_with_valid_credentials(page):
    assert page.locator('a[class*=shopping]').all()
    assert page.locator('//button[text()="Add to cart"]').all()


def test_login_with_invalid_credentials(ui_page):
    ui_page.goto('https://www.saucedemo.com')
    ui_page.locator('[placeholder="Username"]').type('invalid_user')
    ui_page.locator('[placeholder="Password"]').type('no_sauce')
    ui_page.locator('#login-button').click()
    assert ui_page.locator('[data-test="error"]').all()


def test_add_to_cart(page):
    item = page.locator('.inventory_item_name').nth(0).inner_text()
    page.locator('#add-to-cart-sauce-labs-backpack').click()
    page.locator('a[class*=shopping]').click()
    assert page.locator('.inventory_item_name').nth(0).inner_text() == item


def test_add_to_cart_from_product_page(page):
    page.locator('.inventory_item_name').nth(0).click()
    item = page.locator('.inventory_details_name').inner_text()
    page.locator('#add-to-cart-sauce-labs-backpack').click()
    page.locator('a[class*=shopping]').click()
    assert page.locator('.inventory_item_name').nth(0).inner_text() == item


def test_remove_from_cart(page):
    page.locator('#add-to-cart-sauce-labs-backpack').click()
    page.locator('a[class*=shopping]').click()
    page.locator('#remove-sauce-labs-backpack').click()
    assert not page.locator('.cart_item').all()


def test_product_sorting(page):
    sel = page.locator('select.product_sort_container')
    # A to Z
    sel.select_option('az')
    sorted_titles = [i.inner_text() for i in page.locator('.inventory_item_name').all()]
    assert sorted(sorted_titles) == sorted_titles
    # Z to A
    sel.select_option('za')
    reverse_sorted_titles = [i.inner_text() for i in page.locator('.inventory_item_name').all()]
    assert sorted(reverse_sorted_titles, reverse=True) == reverse_sorted_titles
    # low to high
    sel.select_option('lohi')
    sorted_prices = [float(i.inner_text().replace('$', '')) for i in page.locator('.inventory_item_price').all()]
    assert sorted(sorted_prices) == sorted_prices
    # high to low
    sel.select_option('hilo')
    reverse_sorted_prices = [float(i.inner_text().replace('$', '')) for i in
                             page.locator('.inventory_item_price').all()]
    assert sorted(reverse_sorted_prices, reverse=True) == reverse_sorted_prices


def test_checkout_cart(page):
    page.locator('#add-to-cart-sauce-labs-backpack').click()
    page.locator('a[class*=shopping]').click()
    page.locator('#checkout').click()
    page.locator('#first-name').type('Homer')
    page.locator('#last-name').type('Simpson')
    page.locator('#postal-code').type('00000')
    page.locator('#continue').click()
    page.locator('#finish').click()
    assert "complete" in page.locator('.title').inner_text().lower()
    assert page.locator('.complete-header').all()
    assert page.locator('.complete-text').all()
