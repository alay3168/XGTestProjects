import unittest
from selenium import webdriver
import time
from BoxWebAutoTest.pageManager.LoginPage import LoginPage
from BoxWebAutoTest.common import Common as cc
from selenium.webdriver.common.by import By
import TestCaseInfo

class Test_LoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = cc.baseUrl()

    def test_LoginPage_Normal(self):
        # 打开页面
        self.driver.get(self.base_url)
        # 打开登录页面
        login_page = LoginPage(self.driver)
        login_page.driver.implicitly_wait(30)
        # 输入用户名和密码进行登录
        login_page.set_username("admin")
        login_page.set_password("123456")
        login_page.click_SignIn()
        time.sleep(3)
        #登录成功判断
        self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, ".cam-nums > span").text,"今日抓拍总计：10000张",msg='登录失败')

    def test_LoginPage_Wrong_pwd(self):
        # 打开页面
        self.driver.get(self.base_url)
        # 打开登录页面
        login_page = LoginPage(self.driver)
        login_page.driver.implicitly_wait(30)
        # 输入正确用户名和错误密码进行登录
        login_page.set_username("admin")
        login_page.set_password("123123")
        time.sleep(1)
        login_page.click_SignIn()
        time.sleep(3)
        #密码输入错误给出提示
        self.assertEqual(self.driver.find_element(By.CSS_SELECTOR, "body > div.el-message.el-message--error > p").text,"用户名或密码错误",msg='用户名或密码错误')

    def tearDown(self):
        self.driver.close()
        self.driver.quit()

if __name__ == '__main__':
        unittest.main()


