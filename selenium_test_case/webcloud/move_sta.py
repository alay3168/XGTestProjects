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


class Move(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #移动文件    
    def test_file(self):
        u"""移动文件到文件夹"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)
            

        #选择文件
        we.findsCss(driver,"input[type=checkbox]").pop().click()
        time.sleep(2)
        
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        liss = we.findsTagName(driver,"li")
        for li in liss:
            if li.get_attribute('data-action') == 'move':
                li.click()       
        time.sleep(2) 

        #we.findXpath(driver,"/html/body/div[2]/div[2]/div/ul/li[2]").click()
        we.findXpath(driver,"//ul[@class='hx']/li[2]").click()
        time.sleep(3)
        we.findClassName(driver,"h_qd").click()
        time.sleep(2)

        we.findClassName(driver,"collect").click()
        time.sleep(3)
        

        #退出
        login.logout(self)
            
        

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(Move("test_file"))
    #suite.addTest(Restore("test_restore"))

    
    results = unittest.TextTestRunner().run(suite)


        
    

