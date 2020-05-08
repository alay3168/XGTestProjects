#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.time_config_page import TimeConfigPage
from WebPage.main_menu_left_page import MainMenuLeftPage
from Common import common as cc
from ddt import ddt,file_data

case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))
@ddt
class TestTimeConfigPage(unittest.TestCase):
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
        homePage = HomePage(cls.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(cls.driver)
        mainMenuLeftPage.click_systemManageMenu()
        mainMenuLeftPage.click_timeSetMenu()

    def test_0_timezone(self):
        timeConfigPage = TimeConfigPage(self.driver)
        time.sleep(1)
        timeConfigPage.wait_eml_presence(timeConfigPage.timezoneDownBox)
        timeConfigPage.click_timezoneDownBox()
        timeConfigPage.select_timezoneDownBoxSub()
        timeConfigPage.click_saveButton()
        time.sleep(1)
        timeConfigPage.wait_eml_presence(timeConfigPage.saveSuccessToast)
        text = timeConfigPage.get_saveSuccessToast()
        self.assertEqual('保存成功',text,msg = '时间设置页码修改时区配置项保存时失败')

    @file_data(case_yml + "\\time_NTP_config.yaml")
    def test_1_NTP_calibration(self,**test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        timeConfigPage = TimeConfigPage(self.driver)
        time.sleep(1)
        timeConfigPage.wait_eml_presence(timeConfigPage.timezoneDownBox)
        timeConfigPage.select_ntpSetTimeTab()
        timeConfigPage.clear_serverIpAddrField()
        timeConfigPage.clear_ntpPortField()
        timeConfigPage.clear_timeIntervalField()
        timeConfigPage.click_saveButton()
        serverIpAddrErrToast = timeConfigPage.get_serverIpAddrErrToast()
        self.assertEqual('请输入服务器地址',serverIpAddrErrToast,msg = '不输入NTP服务器地址保存失败时断言失败')
        ntpPortErrToast = timeConfigPage.get_ntpPortErrToast()
        self.assertEqual('请输入NTP端口',ntpPortErrToast,msg = '不输入NTP端口保存失败时断言失败')
        timeIntervalErrToast = timeConfigPage.get_timeIntervalErrToast()
        self.assertEqual('请输入校时间隔',timeIntervalErrToast,msg='不输入NTP校时间隔保存失败时断言失败')

        time.sleep(1)
        timeConfigPage.set_serverIpAddrField(test_data.get('NTPServerIP'))
        timeConfigPage.set_ntpPortField(test_data.get('NTPPort'))
        timeConfigPage.set_timeIntervalField(test_data.get('timeInterval'))
        timeConfigPage.click_saveButton()

        if '保存成功' in test_data.get('caseDescription'):
            timeConfigPage.wait_eml_presence(timeConfigPage.saveSuccessToast)
            test = timeConfigPage.get_saveSuccessToast()
            self.assertEqual(test_data.get('expected_re'), test, msg=test_data.get('msg'))
            time.sleep(3)
            timeConfigPage.click_testPortButton()
            time.sleep(1)
            text = timeConfigPage.get_saveSuccessToast()
            self.assertEqual('测试成功', text, msg='测试端口时断言失败')

        if '请输入正确格式的NTP端口' in test_data.get('caseDescription'):
            timeConfigPage.wait_eml_presence(timeConfigPage.ntpPortErrToast)
            test = timeConfigPage.get_ntpPortErrToast()
            self.assertEqual(test_data.get('expected_re'), test, msg=test_data.get('msg'))
        if '校时时间间隔应为大于5的整数' in test_data.get('caseDescription'):
            timeConfigPage.wait_eml_presence(timeConfigPage.timeIntervalErrToast)
            test = timeConfigPage.get_timeIntervalErrToast()
            self.assertEqual(test_data.get('expected_re'), test, msg=test_data.get('msg'))
        if '测试端口失败' in test_data.get('caseDescription'):
            timeConfigPage.wait_eml_presence(timeConfigPage.saveSuccessToast)
            test = timeConfigPage.get_saveSuccessToast()
            self.assertEqual(test_data.get('expected_re'), test, msg=test_data.get('msg'))
            time.sleep(3)
            timeConfigPage.click_testPortButton()
            timeConfigPage.wait_eml_presence(timeConfigPage.testPortErrToast)
            text = timeConfigPage.get_testPortErrToast()
            self.assertEqual('Error!', text, msg='测试端口时断言失败')

    def test_2_manual_calibration(self):
        timeConfigPage = TimeConfigPage(self.driver)
        time.sleep(1)
        timeConfigPage.wait_eml_presence(timeConfigPage.mannualSetTimeTab)
        timeConfigPage.select_mannualSetTimeTab()
        timeConfigPage.clear_setTimeField()
        time.sleep(1)
        timeConfigPage.select_syncWithComputerTime()
        timeConfigPage.click_saveButton()
        timeConfigPage.wait_eml_presence(timeConfigPage.saveSuccessToast)
        text = timeConfigPage.get_saveSuccessToast()
        self.assertEqual('保存成功',text,msg = '清空设置时间字段值保存时断言失败')
        timeConfigPage.clear_setTimeField()
        time.sleep(1)
        timeConfigPage.select_syncWithComputerTime()
        timeConfigPage.click_saveButton()
        timeConfigPage.wait_eml_presence(timeConfigPage.saveSuccessToast)
        text = timeConfigPage.get_saveSuccessToast()
        self.assertEqual('保存成功', text, msg='清空设置时间字段值保存时断言失败')

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
        homePage = HomePage(cls.driver)
        homePage.click_logoutButton()
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == '__main__':
    unittest.main()