def test_add_to_cart(driver):
    driver.get("https://coffee-cart.app/")
    coffee = driver.element("div:not([id]) li")
    coffee.element(".cup-body").click()
    assert "1" in driver.element("[href*=cart]").text
    assert coffee.element("small").text in driver.element(".pay").text


def test_coffee_prices(driver):
    driver.get("https://coffee-cart.app/")
    prices = driver.elements("div:not([id]) li small")
    assert len(prices) > 0

    for price in prices:
        assert float(price.text.replace("$", "")) > 0


def test_remove_coffee_from_cart(driver):
    driver.get("https://coffee-cart.app/")
    driver.element("div:not([id]) li .cup-body").click()
    driver.element("[href*=cart]").click()
    driver.element(".delete").click()
    driver.back()
    assert "0" in driver.element("[href*=cart]").text
    assert "$0" in driver.element(".pay").text


def test_update_coffee_quantity(driver):
    driver.get("https://coffee-cart.app/")
    price = float(driver.element("div:not([id]) li small").text.replace("$", ""))
    driver.element("div:not([id]) li .cup-body").click()
    driver.element(".pay").hover()
    driver.element(".list-item [aria-label*=Add]").click()
    assert str(price * 2) in driver.element(".pay").text


def test_coffee_checkout(driver):
    driver.get("https://coffee-cart.app/")
    driver.element('(//*[@class="cup-body"])[3]').click()
    driver.element(".pay").click()
    assert "$0" not in driver.element(".pay").text
    driver.element("#name").send_keys("test")
    driver.element("#email").send_keys("test@example.com")
    driver.element("#submit-payment").click()
    assert "$0" in driver.element(".pay").text


def test_promo_coffee(driver):
    driver.get("https://coffee-cart.app/")
    driver.element("div:not([id]) li .cup-body").click().click().click()
    before_promo = float(driver.element(".pay").text.split()[1].replace("$", ""))
    assert driver.element(".promo").is_displayed()
    driver.element(".yes").click()
    mocha_promo = float(driver.element('//h4[contains(text(), "Mocha")] //small').text.replace("$", "")) / 2
    assert before_promo + mocha_promo == float(driver.element(".pay").text.split()[1].replace("$", ""))
