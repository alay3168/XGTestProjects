#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Account(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = "http://passport.kuaibo.com/login/?referrer=http%3A%2F%2Faccount.kuaibo.com%2F"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_account(self):
        u'''登录快播用户中心'''
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys("pysetest")
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys("123456")
        driver.find_element_by_id("dl_an_submit").click()
        time.sleep(3)
        
        
        #判断用户名
        username = driver.find_element_by_xpath("//*[@id='Nav']/ul/li[4]/a[1]/span").text
        self.assertEqual(u"pysetest", username)
    

    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(Account("test_account"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
