#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re ,sys
sys.path.append("\public")
from public import login
sys.path.append("\package")
from  package import location

class OneSetp(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #去除重复操作用例    
    def test_repeat(self):
        u"""删除重复影片"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self) 

        
        #去除重复操作，点击去重
        ass = we.findsTagName(driver,'a')
        for a in ass:
            if a.get_attribute('data-action') == 'removeAll':
                a.click()
        time.sleep(3)
        we.findXpath(driver,"/html/body/div[2]/div[2]/div[2]/div").click()
        time.sleep(2)

        #退出
        login.logout(self)


    def test_intellect_rename(self):
        u"""智能重命名"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self) 

        #选择文件重命名
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        ass = we.findsTagName(driver,"li")
        for a in ass:
            if a.get_attribute('data-action') == 'renameAll':
                a.click()       
        time.sleep(3)
        #确认
        we.findXpath(driver,"/html/body/div[3]/div[2]/div[2]/div").click()
        time.sleep(2)
    
        #退出
        login.logout(self)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    #suite.addTest(OneSetp("test_repeat"))
    suite.addTest(OneSetp("test_intellect_rename"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
    


                   

