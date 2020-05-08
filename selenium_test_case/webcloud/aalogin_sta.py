#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re ,sys
sys.path.append("\public")
from public import *
sys.path.append("\package")
from  package import location
import  xml.dom.minidom

#引入xml文件
dom = xml.dom.minidom.parse('E:\\selenium_test_case\\data\\info.xml')
root = dom.documentElement
itemlist = root.getElementsByTagName('login')
item = itemlist[0]
username=item.getAttribute("username")


class Login(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #登陆用例    
    def test_login(self):
        u"""用户登陆"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url) 
        
        try:
            login.login(self)  #登录
            user = we.findXpath(driver,"//*[@id='Nav']/ul/li[4]/a[1]/span").text
            self.assertEqual(user,username,msg='login error')
        except AssertionError,msg:
            driver.get_screenshot_as_file("E:\\selenium_test_case\\error\\loginError.png")
            raise msg  
            
        login.logout(self)#退出

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
