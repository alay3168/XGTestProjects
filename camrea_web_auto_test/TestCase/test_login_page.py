#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_login_page.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/19 10:55   xushaohua      1.0         None
'''

import unittest
from selenium import webdriver
from Common import common as cc
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from ddt import ddt,file_data
import time
import os

case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))
@ddt
class TestLoginPage(unittest.TestCase):
    def save_img(self, img_name):  # 错误截图方法，这个必须先定义好
        self.driver.get_screenshot_as_file('{}/{}.png'.format(os.path.abspath(r" E:\PycharmProjects\box_web_auto_test\img"),img_name))

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = cc.baseUrl()

    @file_data(case_yml + "\\login.yaml")
    def test_login_page(self,**test_data):
        #'''这是第一个测试用例'''
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        self.driver.get(self.base_url)
        loginPage = LoginPage(self.driver)
        self.driver.implicitly_wait(30)
        loginPage.set_username(test_data.get('UserName'))
        loginPage.set_password(test_data.get('Passwd'))
        loginPage.click_SignIn()
        time.sleep(2)
        if test_data.get('Passwd') == '123456':
            homePage = HomePage(self.driver)
            homePage.click_mainMenuButton()
            mainMenuEmlText = homePage.get_mainMenuButton()
            self.assertEqual( test_data.get('expected_re1'),mainMenuEmlText, msg=test_data.get('msg'))
            time.sleep(1)
            homePage.click_previewButton()
            previewEmlText = homePage.get_previewButton()
            self.assertEqual( test_data.get('expected_re'),previewEmlText, msg=test_data.get('msg'))
            time.sleep(1)
            homePage.click_logoutButton()
            print("测试完成")
        if test_data.get('Passwd') == '456456':
            errToast = loginPage.get_pwderrToast()
            self.assertEqual(test_data.get('expected_re'),errToast, msg=test_data.get('msg'))
        if len(test_data.get('Passwd')) >20:
            toast = loginPage.get_pwdOverlengthToast()
            self.assertEqual(test_data.get('expected_re'),toast, msg=test_data.get('msg'))
        if len(test_data.get('UserName')) == 0:
            toast = loginPage.get_usenameNulltoast()
            self.assertEqual(test_data.get('expected_re'),toast, msg=test_data.get('msg'))
        if len(test_data.get('Passwd')) == 0:
            toast = loginPage.get_pwdNulltoast()
            self.assertEqual(test_data.get('expected_re'),toast, msg=test_data.get('msg'))

    def tearDown(self):
        time.sleep(2)
        self.driver.close()
        # self.driver.quit()

def testLoginPage_suit():
    suite = unittest.TestSuite()  # 测试套件
    loader = unittest.TestLoader()  # 用例加载器
    test_class = loader.loadTestsFromTestCase(TestLoginPage)  # 加载测试类
    suite.addTest(test_class)  # 测试类添加到测试套件中
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    unittest.main()