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


class Usershare(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #用户分享列表操作用例    
    def test_usershare(self):
        u"""用户分享列表操作（收起，展开，换一组）"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        login.login(self)  #登录

        #收起
        we.findClassName(driver,"down-share").click()
        time.sleep(2)

        #展开
        we.findXpath(driver,"//div[@id='sidebarEl']/a").click()
        time.sleep(2)

        #换一组
        we.findXpath(driver,"//div[@class='share-top']/a").click()
        time.sleep(2)
        we.findXpath(driver,"//div[@class='share-top']/a").click()
        time.sleep(2)
        
        
        login.logout(self)  #退出
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":

    unittest.main()
          

