#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.device_info_page import DeviceInfoPage
from WebPage.main_menu_left_page import MainMenuLeftPage
from Common import common as cc
from ddt import ddt,file_data

case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))
@ddt
class TestDevicesInfoPage(unittest.TestCase):
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

    def test_device_info_page(self,**test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_systemManageMenu()
        mainMenuLeftPage.click_deviceInfoMenu()

        deviceInfoPage = DeviceInfoPage(self.driver)
        deviceName = deviceInfoPage.get_deviceNameField()
        deviceType = deviceInfoPage.get_deviceTypeField()
        hardwareVersion = deviceInfoPage.get_hardwareVersionField()
        macAddress = deviceInfoPage.get_macAddressField()
        serialNumber = deviceInfoPage.get_serialNumberField()
        softwareVersion = deviceInfoPage.get_softwareVersionField()

        if len(deviceName)>0 and len(deviceType)>0 and len(hardwareVersion)>0 and len(macAddress)>0 and len(serialNumber)>0 and len(softwareVersion)>0:
            sign = 1
        else:
            sign = 0

        self.assertEqual(1,sign,msg = '获取版本信息失败')

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
        homePage = HomePage(cls.driver)
        homePage.click_logoutButton()
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == '__main__':
    unittest.main()