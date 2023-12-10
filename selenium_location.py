import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import unittest


class TestSite(unittest.TestCase):
    def test_good_location(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options)
        text = "New York"
        driver.get("http://0.0.0.0:5000/")
        send = driver.find_element("name", "city")
        send.send_keys(text)
        driver.find_element("name", "city").send_keys(Keys.ENTER)
        self.assertTrue(text in driver.page_source)

    def test_bad_location(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options)
        text = "dgadsghfhk"
        driver.get("http://0.0.0.0:5000/")
        send = driver.find_element("name", "city")
        send.send_keys(text)
        driver.find_element("name", "city").send_keys(Keys.ENTER)
        self.assertFalse(text in driver.page_source)
        text = "location doesn't exist"
        self.assertTrue(text in driver.page_source)



