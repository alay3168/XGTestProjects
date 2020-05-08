#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.video_manager_page import VideoManagerPage
from Common import common as cc
from ddt import ddt,file_data


@ddt
class TestVideoManagerPage(unittest.TestCase):

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
        loginPage.click_SignIn()
        cls.driver.implicitly_wait(30)
        homePage = HomePage(cls.driver)
        homePage.click_mainMenuButton()

    def test_0_add_ordinary_Camera(self):
        videoManagerPage = VideoManagerPage(self.driver)
        # list = videoManagerPage.get_video_list()
        # if len(list)>0:
        #     videoManagerPage.click_batchDeleteRadio()
        #     time.sleep(0.5)
        #     videoManagerPage.click_batchDeleteButton()
        #     time.sleep(0.5)
        #     videoManagerPage.click_batchDeleteConfirmButton()
        #     time.sleep(2)
        videoManagerPage.click_manualAddButton()
        ipStreamAddPage = videoManagerPage.IpStreamAdd(self.driver)
        ipStreamAddPage.wait_eml_presence(videoManagerPage.IpStreamAdd.cameraType)
        # WebDriverWait(self.driver, 5, 0.2).until(lambda x: x.find_element_by_xpath('//*[@id="pane-first"]/form/div[1]/div/div/div/input'))
        ipStreamAddPage.click_cameraType()
        ipStreamAddPage.wait_eml_presence(videoManagerPage.IpStreamAdd.ordinaryCameraType)
        # WebDriverWait(self.driver, 5, 0.2).until(
        #     lambda x: x.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/ul/li[2]/span'))
        ipStreamAddPage.select_ordinaryCameraType()
        ipStreamAddPage.set_cameraIpBox('rtsp://10.58.122.171:554/MainStream')
        ipStreamAddPage.set_userName('admin')
        ipStreamAddPage.set_userpwd('123456')
        ipStreamAddPage.click_confirmButton()
        # WebDriverWait(self.driver, 5, 0.5).until(
        #     lambda x: x.find_element_by_css_selector('body > div.el-message.el-message--success > p'))
        ipStreamAddPage.wait_eml_presence(videoManagerPage.addCameraSuccessTost)
        text = videoManagerPage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='添加普通摄像机ip流断言失败')
        time.sleep(0.5)

    def test_1_add_seemart_Camera(self):
        videoManagerPage = VideoManagerPage(self.driver)
        videoManagerPage.click_manualAddButton()
        # WebDriverWait(self.driver, 5, 0.2).until(
        #     lambda x: x.find_element_by_xpath('//*[@id="pane-first"]/form/div[2]/div/div[1]/input'))
        ipStreamAddPage = videoManagerPage.IpStreamAdd(self.driver)
        ipStreamAddPage.wait_eml_presence(videoManagerPage.IpStreamAdd.cameraIpBox)
        ipStreamAddPage.set_cameraIpBox('10.58.122.172')
        ipStreamAddPage.set_userName('admin')
        ipStreamAddPage.set_userpwd('123456')
        ipStreamAddPage.click_confirmButton()
        # WebDriverWait(self.driver, 5, 0.2).until(
        #     lambda x: x.find_element_by_css_selector('body > div.el-message.el-message--success > p'))
        ipStreamAddPage.wait_eml_presence(videoManagerPage.addCameraSuccessTost)
        text = videoManagerPage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='添加seemart摄像机ip断言失败')
        time.sleep(0.5)

    def test_2_batch_add_ordinary_Camera(self):
        time.sleep(2)
        videoManPage = VideoManagerPage(self.driver)
        videoManPage.wait_eml_presence(videoManPage.manualAddButton)
        # WebDriverWait(self.driver, 5, 0.2).until(
        #     lambda x: x.find_element_by_css_selector('#app > div > div > section > div > div.app-main > section > div > div.operBtns > button:nth-child(1) > span'))
        videoManPage.click_manualAddButton()
        # WebDriverWait(self.driver, 5, 0.2).until(
        #     lambda x: x.find_element_by_xpath('//*[@id="tab-second"]'))
        ipStreamPage = VideoManagerPage.IpStreamAdd(self.driver)
        ipStreamPage.wait_eml_presence(ipStreamPage.ipAddrMultAdd)
        ipStreamPage.click_ipAddrMultAdd()
        # WebDriverWait(self.driver, 5, 0.2).until(
        #     lambda x: x.find_element_by_xpath('//*[@id="pane-second"]/form/div[1]/div/div/div/input'))
        ipStreamPage.wait_eml_presence(ipStreamPage.mulCameraType)
        ipStreamPage.click_mulCameraType()
        # WebDriverWait(self.driver, 5, 0.2).until(
        #     lambda x: x.find_element_by_css_selector('body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > ul > li:nth-child(2)'))
        ipStreamPage.wait_eml_presence(ipStreamPage.ordinaryCameraMultType)
        ipStreamPage.select_ordinaryCameraMultType()
        ipStreamPage.set_rtstStreamStartBox('rtsp://10.58.122.171:554/MainStream')
        ipStreamPage.set_rtstStreamEndBox('rtsp://10.58.122.172:554/MainStream')
        ipStreamPage.set_userNameoMultBox('admin')
        ipStreamPage.set_pwdoMultBox('admin')
        ipStreamPage.click_confirmButton()
        videoManPage.wait_eml_presence(videoManPage.addCameraSuccessTost)
        text = videoManPage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='批量添加普通摄像机断言失败')

    def test_3_batch_add_seemart_Camera(self):
        videoManagerPage = VideoManagerPage(self.driver)
        WebDriverWait(self.driver, 5, 0.2).until(
            lambda x: x.find_element_by_css_selector('#app > div > div > section > div > div.app-main > section > div > div.operBtns > button:nth-child(1) > span'))
        videoManagerPage.click_manualAddButton()
        ipStreamAddPage = videoManagerPage.IpStreamAdd(self.driver)
        WebDriverWait(self.driver, 5, 0.2).until(
            lambda x: x.find_element_by_xpath('//*[@id="tab-second"]'))
        ipStreamAddPage.click_ipAddrMultAdd()
        ipStreamAddPage.set_cameraStartIpMultBox('10.58.122.175')
        ipStreamAddPage.set_cameraEndIpMultBox('10.58.122.176')
        ipStreamAddPage.set_userNameMultBox('admin')
        ipStreamAddPage.set_pwdMultBox('123456')
        ipStreamAddPage.click_confirmButton()
        WebDriverWait(self.driver, 5, 0.5).until(
            lambda x: x.find_element_by_css_selector('body > div.el-message.el-message--success > p'))
        text = videoManagerPage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='批量添加seemart摄像机ip断言失败')
        time.sleep(1)

    def test_4_queryInput(self):
        videoManagerPage = VideoManagerPage(self.driver)
        cameraIpList = videoManagerPage.get_video_list()
        queryIp =0
        if len(cameraIpList)>0:
            if 'rtsp'in cameraIpList[0][1]:
                li = cameraIpList[0][1].split(":")
                queryIp = li[1].split("//")[1]
            else:
                queryIp = cameraIpList[0][1]
        videoManagerPage.query_video(queryIp)
        list = videoManagerPage.get_video_list()
        sign = 0
        if len(list):
            for i in range(len(list)):
                print(list[i][1])
                if queryIp in list[i][1]:
                    sign = 1
                    break
        else:
            sign = 0
        self.assertEqual(1,sign, msg='查询摄像机断言失败')
        homePage = HomePage(self.driver)
        homePage.click_previewButton()
        homePage.click_mainMenuButton()
        time.sleep(2)

    def test_5_editCamera(self):
        videoManagerPage = VideoManagerPage(self.driver)
        delBeforelist = videoManagerPage.get_video_list()
        if len(delBeforelist) >= 0:
            videoManagerPage.click_firstEditorLink()
            time.sleep(1)
            ipStreamAddPage = videoManagerPage.IpStreamAdd(self.driver)
            ipStreamAddPage.set_edtNameBox('公司大门')
            ipStreamAddPage.click_edtFastCaptureRadio()
            ipStreamAddPage.set_edtRemarkBox('编辑摄像机功能测试')
            ipStreamAddPage.click_edtConfirmButton()
            WebDriverWait(self.driver, 5, 0.2).until(lambda x: x.find_element_by_css_selector('body > div.el-message.el-message--success > p'))
            text = videoManagerPage.get_edtSuccessToast()
            self.assertEqual('编辑成功', text, msg='编辑摄像机断言失败')
        else:
            print("记录为空，不能编辑")
        time.sleep(1)

    def test_6_deleteCamera(self):
        videoManagerPage = VideoManagerPage(self.driver)
        delBeforelist = videoManagerPage.get_video_list()
        if len(delBeforelist) >= 0:
            videoManagerPage.click_firstRecordDeleteLink()
            time.sleep(1)
            text = videoManagerPage.get_delSuccessToast()
            self.assertEqual('删除成功', text, msg='删除视频记录断言失败')
            defAfterlist = videoManagerPage.get_video_list()

            self.assertEqual(len(delBeforelist)-1, len(defAfterlist), msg='删除视频记录断言失败')
        else:
            print("记录为空，不能删除")
        time.sleep(1)

    def test_7_batchDeleteButt(self):
        videoManagerPage = VideoManagerPage(self.driver)
        cameraIpList = videoManagerPage.get_video_list()
        if len(cameraIpList)>0:
            videoManagerPage.click_batchDeleteRadio()
            time.sleep(1)
            videoManagerPage.click_batchDeleteButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.batchDeleteConfirmButton)
            # WebDriverWait(self.driver, 5, 0.5).until(
            #     lambda x: x.find_element_by_css_selector('body > div.el-dialog__wrapper.xg-message.delVideoContainer > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span'))
            videoManagerPage.click_batchDeleteConfirmButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.delSuccessToast)
            # WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element_by_css_selector('body > div.el-message.el-message--success > p'))
            text = videoManagerPage.get_delSuccessToast()
            self.assertEqual('删除成功', text, msg='删除视频记录断言失败')
            cameraIpList = videoManagerPage.get_video_list()
            self.assertEqual(0, len(cameraIpList), msg='删除视频记录断言失败')
        time.sleep(1)



    @classmethod
    def tearDownClass(cls):
        homePage = HomePage(cls.driver)
        homePage.click_logoutButton()
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == "__main__":
    unittest.main()