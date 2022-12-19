from typing import Optional, Dict

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait


class AppiumHelper:
    def __init__(
            self,
            command_executor: str = 'http://127.0.0.1:4444/wd/hub',
            desired_capabilities: Optional[Dict] = None,
            wait: int = 10
    ):
        self.driver = webdriver.Remote(command_executor, desired_capabilities)
        self.wait = WebDriverWait(self.driver, wait)

    def id_element(self, path: str):
        return self.wait.until(lambda d: d.find_element(AppiumBy.ID, path))

    def id_elements(self, path: str):
        return self.wait.until(lambda d: d.find_elements(AppiumBy.ID, path))

    def accessibility_element(self, path: str):
        return self.wait.until(lambda d: d.find_element(AppiumBy.ACCESSIBILITY_ID, path))

    def accessibility_elements(self, path: str):
        return self.wait.until(lambda d: d.find_elements(AppiumBy.ACCESSIBILITY_ID, path))

    def xpath_element(self, path: str):
        return self.wait.until(lambda d: d.find_element(AppiumBy.XPATH, path))

    def xpath_elements(self, path: str):
        return self.wait.until(lambda d: d.find_elements(AppiumBy.XPATH, path))

    def press_keycode(self, keycode: int):
        self.driver.press_keycode(keycode)

    def quit(self):
        self.driver.quit()
