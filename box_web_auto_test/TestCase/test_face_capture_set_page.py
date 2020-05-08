#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.main_menu_left_page import MainMenuLeftPage
from WebPage.face_capture_set_page import FaceCaptureSetPage
from Common import common as cc
from ddt import ddt,file_data


case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))

@ddt
class TestFaceCaptureSetPage(unittest.TestCase):
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

    def test_0_face_Capture_Set_Lower(self,**test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_intelligentManageMenu()
        mainMenuLeftPage.wait_eml_presence(mainMenuLeftPage.faceMenu)
        mainMenuLeftPage.click_faceMenu()
        faceCaptureSetPage = FaceCaptureSetPage(self.driver)
        faceCaptureSetPage.wait_eml_presence(FaceCaptureSetPage.picturePushIntervaLower)
        faceCaptureSetPage.click_picturePushIntervaLower()
        faceCaptureSetPage.click_picturePushNumberLower()
        faceCaptureSetPage.click_horizontalAngleLower()
        faceCaptureSetPage.click_pitchingAngleLower()
        faceCaptureSetPage.click_horizontalTiltAngleLower()
        faceCaptureSetPage.click_miniCaptureFaceOptions()
        faceCaptureSetPage.select_miniCaptureFaceOptions60()

        faceCaptureSetPage.click_saveButton()
        time.sleep(1)
        faceCaptureSetPage.wait_eml_presence(FaceCaptureSetPage.saveSuccessToast)
        text = faceCaptureSetPage.get_saveSuccessToast()
        self.assertEqual('保存成功',text,msg = '配置人脸抓参保存失败')

    def test_1_face_Capture_Set_Up(self,**test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_intelligentManageMenu()
        mainMenuLeftPage.wait_eml_presence(mainMenuLeftPage.faceMenu)
        mainMenuLeftPage.click_faceMenu()
        faceCaptureSetPage = FaceCaptureSetPage(self.driver)
        faceCaptureSetPage.wait_eml_presence(FaceCaptureSetPage.picturePushIntervaUp)
        faceCaptureSetPage.click_picturePushIntervaUp()
        faceCaptureSetPage.click_picturePushNumberUp()
        faceCaptureSetPage.click_horizontalAngleUp()
        faceCaptureSetPage.click_pitchingAngleUp()
        faceCaptureSetPage.click_horizontalTiltAngleUp()
        faceCaptureSetPage.click_miniCaptureFaceOptions()
        faceCaptureSetPage.select_miniCaptureFaceOptions100()

        faceCaptureSetPage.click_saveButton()
        time.sleep(1)
        faceCaptureSetPage.wait_eml_presence(FaceCaptureSetPage.saveSuccessToast)
        text = faceCaptureSetPage.get_saveSuccessToast()
        self.assertEqual('保存成功',text,msg = '配置人脸抓参保存失败')

    # @file_data(case_yml + "\\puppyProtocolPage.yaml")
    def test_2_face_Capture_Set_Num(self,**test_data):
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homePage = HomePage(self.driver)
        homePage.click_mainMenuButton()
        time.sleep(2)
        mainMenuLeftPage = MainMenuLeftPage(self.driver)
        mainMenuLeftPage.click_intelligentManageMenu()
        mainMenuLeftPage.wait_eml_presence(mainMenuLeftPage.faceMenu)
        mainMenuLeftPage.click_faceMenu()
        faceCaptureSetPage = FaceCaptureSetPage(self.driver)
        faceCaptureSetPage.wait_eml_presence(FaceCaptureSetPage.picturePushIntervaUp)
        faceCaptureSetPage.clear_picturePushIntervaNum()
        faceCaptureSetPage.clear_picturePushNumberNum()
        faceCaptureSetPage.clear_horizontalAngleNum()
        faceCaptureSetPage.clear_pitchingAngleNum()
        faceCaptureSetPage.clear_horizontalTiltAngleNum()

        text1 = faceCaptureSetPage.get_picturePushIntervaErrToast()
        text2 = faceCaptureSetPage.get_picturePushNumberErrToast()
        text3 = faceCaptureSetPage.get_horizontalAngleErrToast()
        text4 = faceCaptureSetPage.get_pitchingAngleErrToast()
        text5 = faceCaptureSetPage.get_horizontalTiltAngleErrToast()
        faceCaptureSetPage.click_saveButton()

        self.assertEqual('请输入图片推送间隔', text1, msg='不输入图片推送间隔时保存断言失败')
        self.assertEqual('请输入图片推送次数', text2, msg='不输入图片推送次数时保存断言失败')
        self.assertEqual('请输入水平偏转角度', text3, msg='不输入图片水平偏转角度时保存断言失败')
        self.assertEqual('请输入俯仰偏转角度', text4, msg='不输入图片俯仰偏转角度保存断言失败')
        self.assertEqual('请输入水平倾斜角度', text5, msg='不输入图片水平倾斜角度时保存断言失败')

        faceCaptureSetPage.set_picturePushIntervaNum(1000)
        faceCaptureSetPage.set_picturePushNumberNum(2)
        faceCaptureSetPage.set_horizontalAngleNum(30)
        faceCaptureSetPage.set_horizontalTiltAngleNum(30)
        faceCaptureSetPage.set_pitchingAngleNum(60)
        faceCaptureSetPage.click_miniCaptureFaceOptions()
        faceCaptureSetPage.select_miniCaptureFaceOptions30()

        faceCaptureSetPage.click_saveButton()
        time.sleep(1)
        faceCaptureSetPage.wait_eml_presence(FaceCaptureSetPage.saveSuccessToast)
        text = faceCaptureSetPage.get_saveSuccessToast()
        self.assertEqual('保存成功',text,msg = '配置人脸抓参保存失败')

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
        homePage = HomePage(cls.driver)
        homePage.click_logoutButton()
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == '__main__':
    unittest.main()