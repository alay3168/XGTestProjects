#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re ,sys

sys.path.append("\public")
from public import login

sys.path.append("\package")
from  package import location


class Collection(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #收藏热门合集用例    
    def test_heji(self):
        u"""收藏热门合集"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        login.login(self)  #登录

        we.findClassName(driver,"bg-hot").click()
        time.sleep(2)
        we.findClassName(driver,"collect-img").click()
        time.sleep(2)
        we.findXpath(driver,"//div[@class='main-content']/ul/ul/li/a").click()
        time.sleep(3)
        t = we.findClassName(driver,"ok-collect").text

        try:
            self.assertEqual(t,u"收藏成功",msg='hot collect error!')
        except AssertionError,msg:
            driver.get_screenshot_as_file("E:\\selenium_test_case\\error\\colleError.png")
            raise msg
        time.sleep(2)
        we.findClassName(driver,"webcloud-tips-close").click()

        login.logout(self)  #退出
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":

    unittest.main()
          

