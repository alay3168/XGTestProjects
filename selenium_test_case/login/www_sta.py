#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Www(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = "http://passport.kuaibo.com/login/?referrer=http%3A%2F%2Fwww.kuaibo.com%2F"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_www(self):
        u'''登录快播www官网首页'''
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys("pysetest")
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys("123456")
        driver.find_element_by_id("dl_an_submit").click()
        time.sleep(3)
        
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(Www("test_www"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
