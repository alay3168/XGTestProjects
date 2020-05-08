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
from WebPage.tcpip_page import TcpIpPage
from WebPage.main_menu_left_page import MainMenuLeftPage
from Common import common as cc
from ddt import ddt,file_data

case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))

@ddt
class TestTcpIpPage(unittest.TestCase):

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

    @file_data(case_yml + "\\ManualTcpIpconfig.yaml")
    def test_manualTcpIpconfig(self,**test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_networkProtocolMenu()
        mainMenuLeftPage.click_tcpIpMenu()
        self.driver.implicitly_wait(30)
        tcpIpPage = TcpIpPage(self.driver)
        tcpIpPage.clear_ipV4AddrField()
        tcpIpPage.clear_subnetMaskField()
        tcpIpPage.clear_defaultGatewayField()
        tcpIpPage.clear_firstDNSField()
        tcpIpPage.clear_backDNSField()
        time.sleep(1)
        tcpIpPage.set_ipV4AddrField(test_data.get('pV4AddrField'))
        tcpIpPage.set_subnetMaskField(test_data.get('subnetMaskField'))
        tcpIpPage.set_defaultGatewayField(test_data.get('defaultGatewayField'))
        tcpIpPage.set_firstDNSField(test_data.get('firstDNSField'))
        tcpIpPage.set_backDNSField(test_data.get('backDNSField'))
        tcpIpPage.click_saveButton()
        if '成功保存' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.saveSuccessToast))
            text = tcpIpPage.get_saveSuccessToast()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入IPV4地址' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.ipV4AddrNullMessage))
            text = tcpIpPage.get_ipV4AddrNullMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入正确的IPV4地址' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.ipV4AddrErrMessage))
            text = tcpIpPage.get_ipV4AddrErrMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入子网掩码' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.subnetMaskNullMessage))
            text = tcpIpPage.get_subnetMaskNullMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入正确的子网掩码' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.subnetMaskErrMessage))
            text = tcpIpPage.get_subnetMaskErrMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入默认网关' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.defaultGatewayNullMessage))
            text = tcpIpPage.get_defaultGatewayNullMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入正确的默认网关' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.defaultGatewayErrMessage))
            text = tcpIpPage.get_defaultGatewayErrMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入首选DNS' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.firstDNSNullMessage))
            text = tcpIpPage.get_firstDNSNullMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入正确的首选DNS' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.firstDNSErrMessage))
            text = tcpIpPage.get_firstDNSErrMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

        if '请输入正确的备选DNS' in test_data.get('caseDescription'):
            WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(TcpIpPage.backDNSErrMessage))
            text = tcpIpPage.get_backDNSErrMessage()
            self.assertEqual(test_data.get('expected_re'), text, msg=test_data.get('msg'))

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
        homePage = HomePage(cls.driver)
        homePage.click_logoutButton()
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == "__main__":
    unittest.main()