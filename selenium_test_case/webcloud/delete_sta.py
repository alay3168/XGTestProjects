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

class Delete(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

        #删除文件到回收站    
    def test_delete(self):
        u"""删除文件，文件夹到回收站"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        #登录
        login.login(self)

                     
        #删除操作
        we.findClassName(driver,"list-t").click()
        
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        ass = we.findsTagName(driver,"li")
        for a in ass:
            if a.get_attribute('data-action') == 'dele':
                a.click()       
        time.sleep(4)
            
        #退出
        login.logout(self)
            
            
    #一键清空回收站
    def test_empty(self):
        u"""一键清空回收站"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)
        #登陆
        login.login(self) 

        
        #点击清空按钮
        we.findClassName(driver,"clear-tip").click()
        time.sleep(2)
        #driver.find_element_by_class_name("msg-box-panel").find_element_by_xpath("/div[@class='action']/div").click()
        we.findXpath(driver,"/html/body/div[2]/div[2]/div[2]/div").click()
        time.sleep(4)
         
        #退出
        login.logout(self)
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.main()

    # 构造测试集
    suite = unittest.TestSuite()
    
    suite.addTest(Delete("test_delete"))
    suite.addTest(Delete("test_empty"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)

 
          

