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


class Movie(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #收藏热门电影用例    
    def test_dianying(self):
        u"""收藏热门电影"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        login.login(self)  #登录

        we.findClassName(driver,"bg-hot").click()
        time.sleep(2)
        we.findLinkText(driver,u"电影").click()
        time.sleep(2)
        we.findXpath(driver,"//div[@id='hotPanel']/div[2]/ul/li/div").click()
        #we.findClassName(driver,"hot-collect").click()#收藏到私有云
        time.sleep(2)
        #返回私有云
        we.findClassName(driver,"back-btn").click()
        time.sleep(2)  
        
        login.logout(self)  #退出
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":

    unittest.main()
          

