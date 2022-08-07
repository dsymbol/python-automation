from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from typing import Optional, Dict
import os
import sqlite3
import string
from pathlib import Path
from random import choice


def random_password(length: int = 10):
    selection = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    return "".join([choice(choice(selection)) for _ in range(length)])


def random_person():
    database_path = os.path.join(str(Path(__file__).parent), 'people.db')

    if not os.path.exists(database_path):
        raise Exception("Database file not found")

    conn = sqlite3.connect(database_path, check_same_thread=False)
    c = conn.cursor()

    with conn:
        c.execute("""SELECT * FROM people
                     ORDER BY RANDOM()
                     LIMIT 1""")
        result = c.fetchone()
        d = {
            'first_name': result[0],
            'last_name': result[1],
            'address': result[2],
            'city': result[3],
            'state': result[4],
            'zipcode': result[5],
            'sex': result[6],
            'phone': result[7],
            'email_address': result[8],
            'ssn': result[9],
            'birthday': result[10],
            'age': result[11],
            'username': result[12],
            'password': random_password(12)
        }
        return d


class Appium_Helper:
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
