"""
Google AOSP Calculator
"""

import pytest

from utils.helpers import Appium_Helper


@pytest.fixture
def driver():
    desired_caps = {
        "platformName": "Android",
        "appium:deviceName": "Android Emulator",
        "appium:appActivity": "com.android.calculator2.Calculator",
        "appium:appPackage": "com.android.calculator2"
    }
    driver = Appium_Helper("http://127.0.0.1:4723/wd/hub", desired_caps)
    yield driver
    driver.quit()


def test_adding(driver):
    driver.id_element('com.android.calculator2:id/digit_7').click()
    driver.id_element('com.android.calculator2:id/op_add').click()
    driver.id_element('com.android.calculator2:id/digit_6').click()
    driver.id_element('com.android.calculator2:id/eq').click()
    assert driver.id_element('com.android.calculator2:id/result').text == '13'


def test_multiplication(driver):
    driver.id_element('com.android.calculator2:id/digit_5').click()
    driver.id_element('com.android.calculator2:id/op_mul').click()
    driver.id_element('com.android.calculator2:id/digit_5').click()
    driver.id_element('com.android.calculator2:id/eq').click()
    assert driver.id_element('com.android.calculator2:id/result').text == '25'


def test_division(driver):
    driver.id_element('com.android.calculator2:id/digit_8').click()
    driver.id_element('com.android.calculator2:id/digit_1').click()
    driver.id_element('com.android.calculator2:id/op_div').click()
    driver.id_element('com.android.calculator2:id/digit_9').click()
    driver.id_element('com.android.calculator2:id/eq').click()
    assert driver.id_element('com.android.calculator2:id/result').text == '9'


def test_square_root(driver):
    driver.accessibility_element('square root').click()
    driver.id_element('com.android.calculator2:id/digit_3').click()
    driver.id_element('com.android.calculator2:id/digit_6').click()
    driver.id_element('com.android.calculator2:id/eq').click()
    assert driver.id_element('com.android.calculator2:id/result').text == '6'


def test_percent(driver):
    driver.id_element('com.android.calculator2:id/digit_5').click()
    driver.id_element('com.android.calculator2:id/digit_0').click()
    driver.accessibility_element('percent').click()
    [driver.id_element('com.android.calculator2:id/digit_2').click() for _ in range(3)]
    driver.id_element('com.android.calculator2:id/eq').click()
    assert driver.id_element('com.android.calculator2:id/result').text == '111'


def test_power(driver):
    driver.id_element('com.android.calculator2:id/digit_3').click()
    driver.accessibility_element('power').click()
    driver.id_element('com.android.calculator2:id/digit_4').click()
    assert driver.id_element('com.android.calculator2:id/result').text == '81'


def test_long_equation(driver):
    driver.id_element('com.android.calculator2:id/digit_5').click()
    driver.accessibility_element('left parenthesis').click()
    driver.id_element('com.android.calculator2:id/digit_8').click()
    driver.accessibility_element('minus').click()
    driver.id_element('com.android.calculator2:id/digit_2').click()
    driver.accessibility_element('right parenthesis').click()
    driver.accessibility_element('divide').click()
    driver.id_element('com.android.calculator2:id/digit_6').click()
    driver.id_element('com.android.calculator2:id/op_add').click()
    driver.id_element('com.android.calculator2:id/digit_3').click()
    driver.id_element('com.android.calculator2:id/digit_1').click()
    driver.accessibility_element('power').click()
    driver.id_element('com.android.calculator2:id/digit_2').click()
    assert driver.id_element('com.android.calculator2:id/result').text == '966'
