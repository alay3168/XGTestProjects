#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re ,sys
sys.path.append("\public")
from public import login ,openpage

sys.path.append("\package")
from  package import location

class OPmove(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = openpage.openurl(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #用例    
    def test_move(self):
        u"""收藏热门电影到我的私有云"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url) 
        openpage.login(self)  #登录
        #翻页
        we.findId(driver,"next_one").click()
        time.sleep(1)
        we.findId(driver,"pre_one").click()
        time.sleep(1)
        #收藏
        we.findClassName(driver,"hot-img").click()
        time.sleep(2)
            
        openpage.logout(self)#退出

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
