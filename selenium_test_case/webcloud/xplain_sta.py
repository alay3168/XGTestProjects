#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, sys, re 
from time import sleep

sys.path.append("\public")
from public import login

sys.path.append("\package")
from  package import location


class Xplain(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.webcloud_url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #用户登录用例    
    def test_xplain(self):
        u"""使用私有云引导说明"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        driver.maximize_window()
        sleep(3)
        #电脑上用
        we.findClassName(driver,"pc").click()
        sleep(2)
        #driver.find_element_by_class_name("phone-guide").click()
        #we.findClassName(driver,"phone-guide").click()
        #sleep(2)
        we.findXpath(driver,"/html/body/div[3]/div[3]/a").click()
        #we.findClassName(driver,"close-btn").click()
        sleep(2)
        #手机上用
        we.findClassName(driver,"phone").click()
        sleep(2)
        #we.findClassName(driver,"pc-guide").click()
        #sleep(2)
        we.findXpath(driver,"/html/body/div[3]/div[2]/a").click()
        sleep(2)
        
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":

    unittest.main()
          

