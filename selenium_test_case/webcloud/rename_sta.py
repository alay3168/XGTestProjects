#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, sys
sys.path.append("\public")
from public import login

sys.path.append("\package")
from  package import location

class Rename(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_rename(self):
        u"""文件/文件重命名回车确认"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)

        #选择文件重命名
        we.findClassName(driver,"list-t").click()
        time.sleep(3)
        
        element=we.findClassName(driver,"more-fe")
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(2)

        lis=we.findsTagName(driver,'li')
        for li in lis:
            if li.get_attribute('data-action') == 'rename':
                li.click()
        time.sleep(2)

        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u"ipkasdf重命名文件")
                input.send_keys(Keys.ENTER)#回车确认重命名
                time.sleep(2)
        
        #退出
        login.logout(self)
        
    def test_rename2(self):
        u"""文件/文件重命名确认按钮确认"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)

        #选择文件重命名
        we.findClassName(driver,"list-t").click()
        time.sleep(3)
        
        element=we.findClassName(driver,"more-fe")
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(2)

        lis=we.findsTagName(driver,'li')
        for li in lis:
            if li.get_attribute('data-action') == 'rename':
                li.click()
        time.sleep(2)

        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u"aa重命名文件cc")
                we.findLinkText(driver,u"确认").click()#点击确认按钮
                time.sleep(2)
        
        #退出
        login.logout(self)
        

    def test_rename3(self):
        u"""Esc取消文件/文件重命名"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)

        #选择文件重命名
        we.findClassName(driver,"list-t").click()
        time.sleep(3)
        
        element=we.findClassName(driver,"more-fe")
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(2)

        lis=we.findsTagName(driver,'li')
        for li in lis:
            if li.get_attribute('data-action') == 'rename':
                li.click()
        time.sleep(2)

        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u"aa重命名文件cc")
                input.send_keys(Keys.ESCAPE)#Esc取消文件/文件重命名
                
                time.sleep(2)
        
        #退出
        login.logout(self)

        
    def test_rename4(self):
        u"""取消按钮文件/文件重命名"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)

        #选择文件重命名
        we.findClassName(driver,"list-t").click()
        time.sleep(3)
        
        element=we.findClassName(driver,"more-fe")
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(2)

        lis=we.findsTagName(driver,'li')
        for li in lis:
            if li.get_attribute('data-action') == 'rename':
                li.click()
        time.sleep(2)

        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u"aa重命名文件cc")
                we.findLinkText(driver,u"取消").click() #取消按钮
                time.sleep(2)
        

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.main()
    
    suite = unittest.TestSuite()
        
    suite.addTest(Rename("test_rename"))
    suite.addTest(Rename("test_rename2"))
    suite.addTest(Rename("test_rename3"))
    suite.addTest(Rename("test_rename4"))
    
    results = unittest.TextTestRunner().run(suite)
    


                   

