#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://passport.kuaibo.com/login/user/login/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login1(self):
        u'''用户名、密码都为空'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("dl_an_submit").click()
        self.assertEqual(u"帐号不可少于3位", driver.find_element_by_id("wrong_text").text)
        time.sleep(2)
    
    def test_login2(self):
        u'''用户名123，密码为空'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys('123')
        driver.find_element_by_id("dl_an_submit").click()
        self.assertEqual(u"密码不正确", driver.find_element_by_id("wrong_text").text)
        time.sleep(2)

    def test_login3(self):
        u'''用户名为空，密码123'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys('123')
        driver.find_element_by_id("dl_an_submit").click()
        self.assertEqual(u"帐号不可少于3位", driver.find_element_by_id("wrong_text").text)
        time.sleep(2)

    def test_login4(self):
        u'''用户名123，密码123'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys('123')
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys('123')
        driver.find_element_by_id("dl_an_submit").click()
        self.assertEqual(u"密码不正确", driver.find_element_by_id("wrong_text").text)
        time.sleep(2)

    def test_login5(self):
        u'''用户名test360test360，密码123456'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys('test360test360')
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys('123456')
        driver.find_element_by_id("dl_an_submit").click()
        self.assertEqual(u"用户不存在", driver.find_element_by_id("wrong_text").text)
        time.sleep(2)

    def test_login5(self):
        u'''用户名testing360，密码123456'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys('testing360')
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys('123456')
        driver.find_element_by_id("dl_an_submit").click()
        time.sleep(2)
        self.assertEqual(u"密码不正确", driver.find_element_by_id("wrong_text").text)
        time.sleep(2)


    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestSuite()
    #suite.addTest(LoginTest("test_login1"))
    suite.addTest(LoginTest("test_login5"))
    #suite.addTest(LoginTest("test_login3"))

    runner = unittest.TextTestRunner()
    runner.run(suite)






