#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.system_maintenance_page import SysMaintenancePage
from WebPage.main_menu_left_page import MainMenuLeftPage
from WebPage.device_info_page import DeviceInfoPage
from Common import common as cc
from ddt import ddt,file_data

case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))
@ddt
class TestSystemMaintenancePage(unittest.TestCase):
    # options = webdriver.ChromeOptions()
    # prefs = {
    #     "download.prompt_for_download": False,
    #     'download.default_directory': 'C:\\Users\\admin\\Downloads',  # 下载目录
    #     "plugins.always_open_pdf_externally": True,
    #     'profile.default_content_settings.popups': 1,  # 设置为0，禁止弹出窗口
    #     # 'profile.default_content_setting_values.images': 2,#禁止图片加载
    # }
    #
    # options.add_experimental_option('prefs', prefs)
    parametersFile = 'E:\\PycharmProjects\\box_web_auto_test\\TestData\\boxcfg.bin'
    upgradeFile1 = 'E:\\PycharmProjects\\box_web_auto_test\\TestData\\xgai1.bin'
    upgradeFileVersion1 = 'v1.0.0.20200413190100'
    upgradeFile2 = 'E:\\PycharmProjects\\box_web_auto_test\\TestData\\xgai2.bin'
    upgradeFileVersion2 = 'v1.0.0.20200413185500'

    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(chrome_options=self.options)
        self.base_url = cc.baseUrl()
        self.driver.get(self.base_url)
        loginPage = LoginPage(self.driver)
        self.driver.implicitly_wait(30)
        loginPage.set_username('admin')
        loginPage.set_password('123456')
        loginPage.click_SignIn()
        self.driver.implicitly_wait(30)
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_localMenu()
        mainMenuLeftPage.click_systemMaintenanceMenu()

    def test_system_restart(self):
        sysMaintenancePage = SysMaintenancePage(self.driver)
        sysMaintenancePage.click_restartButton()
        sysMaintenancePage.wait_eml_presence(sysMaintenancePage.restartconfirmButton)
        sysMaintenancePage.click_restartconfirmButton()
        time.sleep(60)
        loginpage = LoginPage(self.driver)
        loginpage.wait_eml_presence(loginpage.login)
        text = loginpage.get_login()
        self.assertEqual('登录',text,msg = '重启时断言失败')

    # def test_factory_reset(self):
    #     pass

    def test_export_parameters(self):
        fname = 'C:\\Users\\admin\\Downloads\\boxcfg.bin'
        flag = os.path.isfile(fname)
        if flag :
            os.remove(fname)
        sysMaintenancePage = SysMaintenancePage(self.driver)
        sysMaintenancePage.click_exportParamentButton()
        time.sleep(5)
        fname = 'C:\\Users\\admin\\Downloads\\boxcfg.bin'
        flag = os.path.isfile(fname)
        self.assertEqual(True,flag,msg = '系统维护下载配置文件断言失败')

    def test_import_parameters(self):
        sysMaintenancePage = SysMaintenancePage(self.driver)
        sysMaintenancePage.click_addParamentFileButton(self.parametersFile)
        time.sleep(1)
        sysMaintenancePage.wait_eml_presence(sysMaintenancePage.addFileToast)
        text = sysMaintenancePage.get_addFileToast()
        self.assertEqual('添加文件成功',text,msg = '添加参数文件失败')
        time.sleep(1)
        sysMaintenancePage.click_improtParamentButton()
        time.sleep(2)
        sysMaintenancePage.wait_eml_presence(sysMaintenancePage.importToast)
        text = sysMaintenancePage.get_importToast()
        self.assertEqual('导入完成，正在重启...',text,msg = '导入参数文件时没有提示导入完成需要重启')
        time.sleep(60)
        loginpage = LoginPage(self.driver)
        loginpage.wait_eml_presence(loginpage.login)
        text = loginpage.get_login()
        self.assertEqual('登录', text, msg='导入参数文件重启失败')

    def test_system_upgrade(self):
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_systemManageMenu()
        time.sleep(1)
        mainMenuLeftPage.click_deviceInfoMenu()
        deviceInfoPage = DeviceInfoPage(self.driver)
        time.sleep(1)
        version = deviceInfoPage.get_softwareVersionField()
        if version == self.upgradeFileVersion1:
            mainMenuLeftPage.click_localMenu()
            mainMenuLeftPage.click_systemMaintenanceMenu()
            sysMaintenancePage = SysMaintenancePage(self.driver)
            sysMaintenancePage.click_addUpgradeFileButton(self.upgradeFile2)
            time.sleep(2)
            sysMaintenancePage.wait_eml_presence(sysMaintenancePage.addFileToast)
            text = sysMaintenancePage.get_addFileToast()
            self.assertEqual('添加文件成功', text, msg='添加参数文件失败')
            sysMaintenancePage.click_sysUpgradeButton()
            time.sleep(5)
            sysMaintenancePage.wait_eml_presence(sysMaintenancePage.uploadFileToast)
            text = sysMaintenancePage.get_uploadFileToast()
            self.assertEqual('正在上传...', text, msg='点击升级按钮时没有给出上传文件提示')
            while True:
                time.sleep(1)
                text = sysMaintenancePage.get_uploadScheduleToast()
                print(text,end=', ')
                if text == '99%':
                    break
                else:
                    continue
            time.sleep(10)
            sysMaintenancePage.wait_eml_presence(sysMaintenancePage.upgradeToRestartToast)
            text = sysMaintenancePage.get_upgradeToRestartToast()
            self.assertEqual('正在升级，请勿断电，三分钟后请重新登录。',text,msg = '升级上传文件完成后没有给出正在升级提示')
            time.sleep(180)
            loginpage = LoginPage(self.driver)
            loginpage.wait_eml_presence(loginpage.login)
            text = loginpage.get_login()
            self.assertEqual('登录', text, msg='导入参数文件重启失败')
        else:
            mainMenuLeftPage.click_localMenu()
            mainMenuLeftPage.click_systemMaintenanceMenu()
            sysMaintenancePage = SysMaintenancePage(self.driver)
            sysMaintenancePage.click_addUpgradeFileButton(self.upgradeFile1)
            time.sleep(2)
            sysMaintenancePage.wait_eml_presence(sysMaintenancePage.addFileToast)
            text = sysMaintenancePage.get_addFileToast()
            self.assertEqual('添加文件成功', text, msg='添加参数文件失败')
            sysMaintenancePage.click_sysUpgradeButton()
            time.sleep(5)
            sysMaintenancePage.wait_eml_presence(sysMaintenancePage.uploadFileToast)
            text = sysMaintenancePage.get_uploadFileToast()
            self.assertEqual('正在上传...', text, msg='点击升级按钮时没有给出上传文件提示')
            while True:
                time.sleep(1)
                text = sysMaintenancePage.get_uploadScheduleToast()
                print(text, end=', ')
                if text == '99%':
                    break
                else:
                    continue
            time.sleep(10)
            sysMaintenancePage.wait_eml_presence(sysMaintenancePage.upgradeToRestartToast)
            text = sysMaintenancePage.get_upgradeToRestartToast()
            self.assertEqual('正在升级，请勿断电，三分钟后请重新登录。', text, msg='升级上传文件完成后没有给出正在升级提示')
            time.sleep(180)
            loginpage = LoginPage(self.driver)
            loginpage.wait_eml_presence(loginpage.login)
            text = loginpage.get_login()
            self.assertEqual('登录', text, msg='导入参数文件重启失败')

    # @classmethod
    def tearDown(self):
        time.sleep(1)
        self.driver.close()
        print("------------执行用例结束-----------")

if __name__ == '__main__':
    unittest.main()