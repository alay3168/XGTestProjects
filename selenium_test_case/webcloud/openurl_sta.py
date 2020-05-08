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

class Openurl(unittest.TestCase):
    
    def setUp(self):
        self.driver = login.browser(self)
        self.we = location
        self.driver.implicitly_wait(30)
        self.base_url = login.url(self)
        self.verificationErrors = []
        self.accept_next_alert = True

    #用户分享操作用例    
    def test_add(self):
        u"""打开文件公开链接，收藏文件到私有云"""
        driver = self.driver
        we = self.we
        driver.get(self.base_url)

        #登陆
        login.login(self)
        
        we.findLinkText(driver,"del").click()
        time.sleep(2)
        
        we.findClassName(driver,"list-t").click()
        time.sleep(2)
        above = we.findClassName(driver,"more-features")
        ActionChains(driver).move_to_element(above).perform()
        time.sleep(2)
        liss = we.findsTagName(driver,"li")
        for li in liss:
            if li.get_attribute('data-action') == 'share':
                li.click()       
        time.sleep(2)
        
        #获得当前窗口
        nowhandle=driver.current_window_handle
        #we.findXpath(driver,"/html/body/div[4]").click()
        time.sleep(2)
        we.findClassName(driver,"link-input").click()
        time.sleep(1)

        #获得所有窗口
        allhandles=driver.window_handles

        for handle in allhandles:
            if handle != nowhandle:
                driver.switch_to_window(handle)
                print 'now register window!'
                #添加文件到私有云
                time.sleep(3)
                we.findId(driver,"pub_collect_a").click()
                time.sleep(5)
                driver.close()

                
        #driver.switch_to_window(nowhandle)

        
        #退出
        #login.logout(self)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(Openurl("test_add"))
        
    results = unittest.TextTestRunner().run(suite)



                   

