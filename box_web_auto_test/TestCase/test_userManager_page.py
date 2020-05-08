#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.user_manage_page import UserManagePage
from WebPage.main_menu_left_page import MainMenuLeftPage
from Common import common as cc
from ddt import ddt,file_data


@ddt
class TestUserManagerPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.set_window_size(1920, 1080)
        cls.base_url = cc.baseUrl()
        cls.driver.get(cls.base_url)
        loginPage = LoginPage(cls.driver)
        cls.driver.implicitly_wait(30)
        loginPage.set_username('admin')
        loginPage.set_password('123456')
        time.sleep(1)
        loginPage.click_SignIn()
        time.sleep(2)
        homePage = HomePage(cls.driver)
        homePage.wait_eml_presence(homePage.mainMenuButton)
        homePage.click_mainMenuButton()
        mainMenuLeftPage = MainMenuLeftPage(cls.driver)
        mainMenuLeftPage.wait_eml_presence(mainMenuLeftPage.userManageMenu)
        mainMenuLeftPage.click_userManageMenu()
        mainMenuLeftPage.wait_eml_presence(mainMenuLeftPage.userMenu)
        mainMenuLeftPage.click_userMenu()

    # def test_0_add_user(self):
    #     userManagPage = UserManagePage(self.driver)
    #     userManagPage.wait_eml_presence(userManagPage.addUserButton)
    #     userManagPage.click_addUserButton()
    #     addUserPage = UserManagePage.AddUserPage(self.driver)
    #     addUserPage.wait_eml_presence(addUserPage.userNameField)
    #     addUserPage.set_userNameField('test')
    #     addUserPage.click_userTypeField()
    #     addUserPage.set_operatorOptionType()
    #     addUserPage.set_pwdField('a123456')
    #     addUserPage.set_pwdConfirmField('a123456')
    #     addUserPage.click_saveButton()
    #     time.sleep(1)
    #     userManagPage.wait_eml_presence(userManagPage.addUserSuccessToast)
    #     msg = userManagPage.get_addUserSuccessToast()
    #     self.assertEqual('保存成功',msg,msg = '添加用户失败')

    # def test_1_modify_user(self):
    #     userManagPage = UserManagePage(self.driver)
    #     userManagPage.wait_eml_presence(userManagPage.addUserButton)
    #     userManagPage.click_modifyUserButton()
    #     modifyUserPage = UserManagePage.ModifyuserPage(self.driver)
    #     modifyUserPage.clear_userName()
    #     modifyUserPage.set_userName('test111')
    #     modifyUserPage.click_saveButton()
    #     userManagPage.wait_eml_presence(userManagPage.addUserSuccessToast)
    #     msg = userManagPage.get_addUserSuccessToast()
    #     self.assertEqual('保存成功', msg, msg='添加用户失败')

    def test_2_delete_user(self):
        userManagPage = UserManagePage(self.driver)
        userManagPage.wait_eml_presence(userManagPage.addUserButton)
        userManagPage.delete_user_list()


    @classmethod
    def tearDownClass(cls):
        homePage = HomePage(cls.driver)
        homePage.click_logoutButton()
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == '__main__':
    unittest.main()