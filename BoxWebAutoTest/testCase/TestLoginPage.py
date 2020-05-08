#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TestLoginPage.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/19 10:55   xushaohua      1.0         None
'''

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from BeautifulReport import BeautifulReport
from selenium.webdriver.common.keys import Keys
from Common import Common as cc
from WebPage.LoginPage import LoginPage
from ddt import ddt,file_data,unpack,data
import yaml

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

    # @BeautifulReport.add_test_img('test_LoginPage_Normal')
    css_selector1 = '#app > div > div > section > div > div.preview-content > div.time-photo > div > div.cam-nums > span'
    expected_re1  = '今日抓拍总计：10000张'
    msg1 = '输入正确用户名和密码断言失败，登录失败'
    caseDescription1 = '输入正确用户名和密码登录'

    css_selector2 = 'body > div.el-message.el-message--error > p'
    expected_re2  = '用户名或密码错误1'
    msg2 = '输入错误的密码登录断言失败'
    caseDescription2 = '输入错误的用户密码进行登录'
    @file_data(case_yml + "\login.yaml")
    def test_LoginPage_Normal(self,**test_data):
        #'''这是第一个测试用例'''
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        self.driver.get(self.base_url)
        loginPage = LoginPage(self.driver)
        self.driver.implicitly_wait(30)
        loginPage.set_username(test_data.get('UserName'))
        loginPage.set_password(test_data.get('Passwd'))
        time.sleep(1)
        loginPage.click_SignIn()

        #断言登录是否成功
        text= self.driver.find_element(By.CSS_SELECTOR,test_data.get('css_selector')).text
        self.assertEqual(text,test_data.get('expected_re'),msg = test_data.get('msg'))

    # # @BeautifulReport.add_test_img('test_LoginPage_errPwd')
    # def test_LoginPage_errPwd(self):
    #     self.driver.get(self.base_url)
    #     loginPage = LoginPage(self.driver)
    #     self.driver.implicitly_wait(30)
    #     loginPage.set_username('admin')
    #     loginPage.set_password('123123')
    #     time.sleep(1)
    #     loginPage.click_SignIn()
    #     text = self.driver.find_element(By.CSS_SELECTOR,
    #                                     'body > div.el-message.el-message--error > p').text
    #     self.assertEqual(text, '用户名或密码错误', msg='输入错误的密码登录断言失败')

    def tearDown(self):
        time.sleep(1)
        self.driver.close()
        # self.driver.quit()

def TestLoginPage_suit():
    suite = unittest.TestSuite()  # 测试套件
    loader = unittest.TestLoader()  # 用例加载器
    test_class = loader.loadTestsFromTestCase(TestLoginPage)  # 加载测试类
    suite.addTest(test_class)  # 测试类添加到测试套件中
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    unittest.main()