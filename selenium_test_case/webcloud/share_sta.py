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

class Share(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #用户分享操作用例    
    def test_share(self):
        u"""分享文件"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)

        #分享操作
        we.findClassName(driver,"public-btn").click()
        time.sleep(3)
        we.findClassName(driver,"share-btn-style").click()
        time.sleep(3)
        we.findClassName(driver,"close-btn").click()
        time.sleep(2)

    #用户分享合集    
    def test_gather(self):
        u"""分享合集"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)

        #分享操作
        we.findLinkText(driver,"test").click()
        time.sleep(3)
        liss=we.findsClassName(driver,"list-t")
        for li in liss:
            li.click()
            time.sleep(0.5)

        #创建合集
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        liss = we.findsTagName(driver,"li")
        for li in liss:
            if li.get_attribute('data-action') == 'share':
                li.click()       
        time.sleep(2)

        #输入合集名字
        we.findClassName(driver,"share-text").send_keys(u"new合集")
        we.findXpath(driver,"//div[@class='link-content']/a").click()
        time.sleep(5)

        
        
        #退出
        login.logout(self)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(Share("test_share"))
    #suite.addTest(Share("test_gather"))
    
    results = unittest.TextTestRunner().run(suite)



                   

