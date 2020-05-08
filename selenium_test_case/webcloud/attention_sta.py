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

class Attention(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

        
    def test_att(self):
        u"""收藏小二私有云文件"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url) 
        login.login(self) #登陆

        we.findClassName(driver,"bg-attention").click()
        time.sleep(2)
        we.findXpath(driver,"/html/body/div/div[2]/div[2]/div[4]/div[4]/table/tbody[3]/tr/td[2]").click()
        time.sleep(2)
        info= we.findClassName(driver,"collect-added").text
        try:
            self.assertEqual(info,u"收藏成功",msg='The collection file failed!')
        except AssertionError,msg:
            raise msg
        
        login.logout(self)#退出

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
