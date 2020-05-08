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


class Restore(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #删除文件到回收站    
    def test_del(self):
        u"""全选文件/文件夹删除到回收站"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)
            

        #删除操作
        we.findCss(driver,"td[class=list-t]").click()
        time.sleep(2)
        
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        liss = we.findsTagName(driver,"li")
        for li in liss:
            if li.get_attribute('data-action') == 'dele':
                li.click()       
        time.sleep(2)

        #收藏一个文件
        #we.findClassName(driver,"collect_span").click()


        #退出
        login.logout(self)
            
        
    def test_restore(self):
        u"""回收站文件还原"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)

        we.findClassName(driver,"recycle-tip").click()
        time.sleep(3)
        we.findXpath(driver,"/html/body/div/div[2]/div[2]/div[2]/div/div[2]/input").click()
        time.sleep(2)

        ass = we.findsTagName(driver,"a")
        for a in ass:
            if a.get_attribute('data-action') == 'restore':
                a.click()
                time.sleep(2)


        #退出
        login.logout(self)
        

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(Restore("test_del"))
    suite.addTest(Restore("test_restore"))

    
    results = unittest.TextTestRunner().run(suite)


        
    

