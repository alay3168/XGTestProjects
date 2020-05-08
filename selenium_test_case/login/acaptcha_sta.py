#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Captcha(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://passport.kuaibo.com/login/user/login/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_captcha1(self):
        u'''用户名，密码错误，出现验证码'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys("testing360")
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys("123456")
        driver.find_element_by_id("dl_an_submit").click()
        time.sleep(3)
        
        #判断验证码是否存在
        for i in range(5):
            try:
                if "" == driver.find_element_by_css_selector("img.captcha_img").text: break
                #if self.is_element_present(By.CLASS_NAME, "captcha_img"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        
        self.assertEqual(u"密码不正确", driver.find_element_by_id("wrong_text").text)
    
    def test_captcha2(self):
        u'''错误的验证码'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("user_name").clear()
        driver.find_element_by_id("user_name").send_keys("testing360")
        driver.find_element_by_id("user_pwd").clear()
        driver.find_element_by_id("user_pwd").send_keys("123456")
        driver.find_element_by_id("dl_an_submit").click()
        time.sleep(1)
        driver.find_element_by_name("captcha").clear()
        driver.find_element_by_name("captcha").send_keys("1111")
        time.sleep(4)
        self.assertEqual(u"验证码错误", driver.find_element_by_id("wrong_text").text)
        time.sleep(2)

    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.mian()

    suite = unittest.TestSuite()

    #suite.addTest(Captcha("test_captcha2"))
    suite.addTest(Captcha("test_captcha1"))

    runner = unittest.TextTestRunner()
    runner.run(suite)

