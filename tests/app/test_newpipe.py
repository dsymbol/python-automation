"""
https://github.com/TeamNewPipe/NewPipe/releases/tag/v0.23.1
"""

import os

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from utils.helpers import Appium_Helper


@pytest.fixture
def driver():
    desired_caps = {
        "platformName": "Android",
        "appium:deviceName": "Android Emulator",
        "appium:app": os.path.abspath("NewPipe_v0.23.1.apk")
    }
    driver = Appium_Helper("http://127.0.0.1:4723/wd/hub", desired_caps)
    driver.wait.until(EC.visibility_of_element_located((AppiumBy.ID, 'org.schabi.newpipe:id/itemRoot')))
    yield driver
    driver.quit()


def test_root_items(driver):
    items = driver.id_elements('org.schabi.newpipe:id/itemRoot')
    assert len(items) > 3
    views = driver.id_elements('org.schabi.newpipe:id/itemAdditionalDetails')
    for i in views:
        text = i.text.split()
        assert "m" in text[0].lower() or "k" in text[0].lower()


def test_search_query(driver):
    keyword = "appium"
    driver.id_element('org.schabi.newpipe:id/action_search').click()
    driver.id_element('org.schabi.newpipe:id/toolbar_search_edit_text').send_keys(keyword)
    driver.press_keycode(66)
    titles = driver.id_elements('org.schabi.newpipe:id/itemVideoTitleView')
    for i in titles:
        assert keyword in i.text.lower()


def test_menu(driver):
    driver.accessibility_element('Open Drawer').click()
    title = driver.id_element('org.schabi.newpipe:id/drawer_header_newpipe_title')
    assert "newpipe" in title.text.lower()
    menu_items = driver.id_elements('org.schabi.newpipe:id/design_menu_item_text')
    menu_items = [i.text.lower() for i in menu_items]
    assert "settings" in menu_items


def test_home_tabs(driver):
    current_tab = driver.xpath_element('//android.widget.ImageButton[@content-desc="Open Drawer"] '
                                       '//following-sibling::android.widget.TextView')
    driver.accessibility_element('Trending').click()
    assert "trending" in current_tab.text.lower()
    driver.accessibility_element('Subscriptions').click()
    assert "subscriptions" in current_tab.text.lower()
    driver.xpath_element('//android.widget.LinearLayout[@content-desc="Bookmarked Playlists"]'
                         '/android.widget.ImageView').click()
    assert "bookmarked" in current_tab.text.lower()


def test_grid_view_mode(driver):
    driver.accessibility_element('Open Drawer').click()
    menu_items = driver.id_elements('org.schabi.newpipe:id/design_menu_item_text')
    [i.click() for i in menu_items if i.text.lower() == "settings"]
    settings_options = driver.id_elements('android:id/title')
    try:
        [i.click() for i in settings_options if i.text.lower() == "appearance"]
    except StaleElementReferenceException:
        pass
    appearance_options = driver.id_elements('android:id/title')
    [i.click() for i in appearance_options if "view mode" in i.text.lower()]
    view_modes = driver.id_elements('android:id/text1')
    [i.click() for i in view_modes if "grid" in i.text.lower()]
    for i in range(2):
        driver.accessibility_element('Navigate up').click()
    driver.wait.until(EC.visibility_of_element_located((AppiumBy.ID, 'org.schabi.newpipe:id/itemRoot')))
    items = driver.id_elements('org.schabi.newpipe:id/itemRoot')
    assert items[0].rect['y'] == items[1].rect['y']
