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

se = open('E:\\selenium_test_case\\data\\seed.txt','r')
seed = se.read()
qvod = 'E:\\selenium_test_case\\data\\snack.qsed'

#print seed
class Addsend(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

        
    def test_qvod(self):
        u"""添加qvod种子文件"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        login.login(self)  #登录

        we.findXpath(driver,"//div[@id='ribbonMenu']/div[3]/a").click()
        time.sleep(2)
        we.findXpath(driver,"//div[@class='tagTitle']/ul/li[2]").click()
        time.sleep(2)
        we.findName(driver,"qsed_file").send_keys(qvod)
        time.sleep(2)
        we.findClassName(driver,"ok-btn").click()
        time.sleep(2)
        
        login.logout(self)  #退出

    def test_seed(self):
        u"""添加快播链接"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        login.login(self)  #登录

        we.findXpath(driver,"//div[@id='ribbonMenu']/div[3]/a").click()
        time.sleep(2)
        we.findName(driver,"textarea").send_keys(seed)
        time.sleep(2)
        we.findClassName(driver,"ok-btn").click()
        time.sleep(2)
        
        login.logout(self)  #退出
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":

    suite = unittest.TestSuite()
    
    suite.addTest(Addsend("test_seed"))
    suite.addTest(Addsend("test_qvod"))

    results = unittest.TextTestRunner().run(suite)

    #unittest.main()
          

