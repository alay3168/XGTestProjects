#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.action_chains import ActionChains
import unittest, time ,sys
sys.path.append("\public")
from public import login
sys.path.append("\package")
from  package import location


class Delete2(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #删除文件    
    def test_delfile(self):
        u"""永久删除单个文件"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)
            

        #选择文件
        we.findsCss(driver,"input[type=checkbox]").pop().click()
        time.sleep(2)

        we.findXpath(driver,"//div[@id='ribbonMenu']/div[3]/a[2]").click()
        time.sleep(2)
        we.findXpath(driver,"//div[@class='action']/div").click()
        time.sleep(2)
 
        #we.findClassName(driver,"collect").click()#添加文件
        #time.sleep(3)
        
        #退出
        login.logout(self)
            
    def test_delfiles(self):
        u"""永久删除单个文件夹"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)
            

        #选择文件
        we.findCss(driver,"td[class=list-t]").click()
        #we.findsCss(driver,"input[type=checkbox]").pop().click()
        time.sleep(2)

        we.findXpath(driver,"//div[@id='ribbonMenu']/div[3]/a[2]").click()
        time.sleep(2)
        we.findXpath(driver,"//div[@class='action']/div").click()
        time.sleep(2)

        
        #退出
        login.logout(self)
        

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(Delete2("test_delfile"))
    suite.addTest(Delete2("test_delfiles"))
    

    
    results = unittest.TextTestRunner().run(suite)


        
    

