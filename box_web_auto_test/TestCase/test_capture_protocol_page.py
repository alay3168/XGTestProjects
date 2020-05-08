#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.capture_protocol_page import CaptureProtocolPage
from WebPage.main_menu_left_page import MainMenuLeftPage
from Common import common as cc
from ddt import ddt,file_data


case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))

@ddt
class TestCaptureProtocolPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.base_url = cc.baseUrl()
        cls.driver.get(cls.base_url)
        loginPage = LoginPage(cls.driver)
        cls.driver.implicitly_wait(30)
        loginPage.set_username('admin')
        loginPage.set_password('123456')
        loginPage.click_SignIn()
        cls.driver.implicitly_wait(30)

    @file_data(case_yml + "\\ftpProtocolPage.yaml")
    def test_FTP_Protocol(self, **test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_networkProtocolMenu()
        mainMenuLeftPage.click_captureProtocolMenu()

        captureProtocolPage = CaptureProtocolPage(self.driver)
        captureProtocolPage.wait_eml_presence(captureProtocolPage.FTPTab)
        captureProtocolPage.select_FTPTab()
        captureProtocolPage.wait_eml_presence(captureProtocolPage.ftpServerIPField)
        captureProtocolPage.clear_ftpServerIPField()
        captureProtocolPage.clear_ftpPortField()
        captureProtocolPage.clear_ftpUserNameField()
        captureProtocolPage.clear_ftpPasswdField()

        captureProtocolPage.set_ftpServerIPField(test_data.get('ftpServerIPField'))
        captureProtocolPage.set_ftpPortField(test_data.get('ftpPortField'))
        captureProtocolPage.set_ftpUserNameField(test_data.get('ftpUserNameField'))
        captureProtocolPage.set_ftpPasswdField(test_data.get('ftpPasswdField'))

        if '上传图片测试失败' in test_data.get('caseDescription'):
            captureProtocolPage.click_ftpUploadTestPicturesButton()
            captureProtocolPage.wait_eml_presence(captureProtocolPage.ftpUploadTestPictureToast)
            text = captureProtocolPage.get_ftpUploadTestPictureToast()
            self.assertEqual('IP或端口号错误', text, msg='输入不错误的FTP服务器地址，上传图片测试断言失败')
            time.sleep(3)
        if '保存成功' in test_data.get('caseDescription'):
            captureProtocolPage.click_ftpUploadTestPicturesButton()
            captureProtocolPage.wait_eml_presence(captureProtocolPage.ftpUploadTestPictureToast)
            text = captureProtocolPage.get_ftpUploadTestPictureToast()
            self.assertEqual('测试成功', text, msg='上传图片测试断言失败')
            time.sleep(3)

        captureProtocolPage.click_ftpSaveButton()
        time.sleep(1)

        if '上传图片测试失败' in test_data.get('caseDescription'):
            captureProtocolPage.wait_eml_presence(captureProtocolPage.saveSuccessToast)
            text = captureProtocolPage.get_saveSuccessToast()
            self.assertEqual(test_data.get('expected_re'), text, msg= test_data.get('msg'))

        if '请输入服务器地址' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_ftpServerIPErrToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入正确的服务器地址' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_ftpServerIPErrToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入端口号' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_ftpPortErrToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '端口号不在1-65535范围内' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_ftpPortErrToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入服务器用户名' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_ftpUserNameErrToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入连接服务器密码' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_fftpPasswdErrToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '保存成功' in test_data.get('caseDescription'):
            captureProtocolPage.wait_eml_presence(captureProtocolPage.saveSuccessToast)
            text = captureProtocolPage.get_saveSuccessToast()
            self.assertEqual(test_data.get('expected_re'), text, msg= test_data.get('msg'))
        time.sleep(1)

    @file_data(case_yml + "\\puppyProtocolPage.yaml")
    def test_puppy_Protocol(self,**test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_networkProtocolMenu()
        mainMenuLeftPage.click_captureProtocolMenu()

        captureProtocolPage = CaptureProtocolPage(self.driver)
        captureProtocolPage.wait_eml_presence(captureProtocolPage.puppyTab)
        captureProtocolPage.select_puppyTab()
        captureProtocolPage.wait_eml_presence(captureProtocolPage.puppyServerIPField)
        captureProtocolPage.clear_puppyServerIPField()
        captureProtocolPage.clear_puppyPortField()
        captureProtocolPage.set_puppyServerIPField(test_data.get('puppyServerIPField'))
        captureProtocolPage.set_puppyPortField(test_data.get('puppyPortField'))
        captureProtocolPage.click_puppySaveButton()

        if '保存成功' in test_data.get('caseDescription'):
            captureProtocolPage.wait_eml_presence(captureProtocolPage.saveSuccessToast)
            text = captureProtocolPage.get_saveSuccessToast()
            self.assertEqual(test_data.get('expected_re'),text,msg = test_data.get('msg'))

        if '请输入服务器地址' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_puppyServerIPErrToast()
            self.assertEqual(test_data.get('expected_re'),text,msg = test_data.get('msg'))

        if '请输入正确的服务器地址' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_puppyServerIPErrToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入端口号' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_puppyPortErrToast()
            self.assertEqual(test_data.get('expected_re'),text,msg = test_data.get('msg'))

        if '请输入正确的端口号' in test_data.get('caseDescription'):
            text = captureProtocolPage.get_puppyPortErrToast()
            self.assertEqual(test_data.get('expected_re'),text,msg = test_data.get('msg'))
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
        homePage = HomePage(cls.driver)
        homePage.click_logoutButton()
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == "__main__":
    unittest.main()