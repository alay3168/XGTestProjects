#! /usr/bin/env python
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re ,sys
sys.path.append("\public")
from public import login

sys.path.append("\package")
from  package import location

class Create(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #新建文件夹    
    def test_create(self):
        u"""新建文件夹确认按钮确认"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        #登录
        login.login(self)


        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        ass = we.findsTagName(driver,"li")
        for a in ass:
            if a.get_attribute('data-action') == 'new':
                a.click()
        time.sleep(2)
                
        #创建文件夹
        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u'文件夹')
        we.findLinkText(driver,u"确认").click() #确认按钮
        time.sleep(3)

        #退出
        login.logout(self)
        
    def test_create2(self):
        u"""新建文件夹回车确认"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        #登录
        login.login(self)

        #创建文件夹
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        ass = we.findsTagName(driver,"li")
        for a in ass:
            if a.get_attribute('data-action') == 'new':
                a.click()
        time.sleep(2)

        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u'文件夹2222')
                input.send_keys(Keys.ENTER) #回车确认
        
        time.sleep(3)

        #退出
        login.logout(self)

    def test_create3(self):
        u"""新建文件夹取消按钮取消"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        #登录
        login.login(self)


        #创建文件夹
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        ass = we.findsTagName(driver,"li")
        for a in ass:
            if a.get_attribute('data-action') == 'new':
                a.click()
        time.sleep(2)

        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u'aa!@#文件夹')
        we.findLinkText(driver,u"取消").click() #取消按钮
        time.sleep(3)

        #退出
        login.logout(self)

    def test_create4(self):
        u"""新建文件夹ESC取消"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        #登录
        login.login(self)

        #创建文件夹
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        ass = we.findsTagName(driver,"li")
        for a in ass:
            if a.get_attribute('data-action') == 'new':
                a.click()
        time.sleep(2)

        inputs=we.findsTagName(driver,'input')
        for input in inputs:
            if input.get_attribute('type') == 'text':
                input.send_keys(u'aa!@#文件夹')
                input.send_keys(Keys.ESCAPE) #ESC取消按钮
                time.sleep(3)

        #退出
        login.logout(self)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(Create("test_create"))
    suite.addTest(Create("test_create2"))
    suite.addTest(Create("test_create3"))
    suite.addTest(Create("test_create4"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    #unittest.main()
