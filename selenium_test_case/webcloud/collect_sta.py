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

class Collect(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #收藏功能用例    
    def test_collect(self):
        u"""收藏用户分享文件"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url) 
        login.login(self) #登陆
        
        inputs=we.findsTagName(driver,'input')
        n=0
        for i in inputs:
            if i.get_attribute('type')=="checkbox":
                n=n+1

        
        #收藏操作
        try:
            we.findClassName(driver,"collect_span").click()
            time.sleep(3)
        except:
            we.findXpath(driver,"//div[@class='main-content']/ul/ul/li/a").click()
            time.sleep(2)
            we.findClassName(driver,"webcloud-tips-close").click()
            time.sleep(2)


        inputs=we.findsTagName(driver,'input')
        ns=0
        for ii in inputs:
            if ii.get_attribute('type')=="checkbox":
                ns=ns+1


        try:
            self.assertEqual(ns,n+1,msg='add file error')
        except Exception, msg:
            raise msg

        
            
        login.logout(self)#退出

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
