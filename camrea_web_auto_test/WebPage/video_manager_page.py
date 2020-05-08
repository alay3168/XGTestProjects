#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   video_manager_page.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 14:30   xushaohua      1.0         None
'''
from selenium.webdriver.common.by import By
from WebPage.base_page import BasePage
import unittest
from selenium import webdriver
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from Common import common as cc
from selenium.webdriver.support.ui import Select
from ddt import ddt,file_data

class VideoManagerPage(BasePage):
    # page element identifier
    queryInputBox = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.operBtns > div > input')
    manualAddButton = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.operBtns > button:nth-child(1) > span')
    batchDeleteButton = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.operBtns > button:nth-child(2) > span')
    batchDeleteRadio = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/div[2]/table/thead/tr/th[1]/div/label/span/span')
    batchDeleteConfirmButton = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-message.delVideoContainer > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span')
    videoAccessEml = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/div/div/span/span[2]/span[1]/span')
    deviceTypeEml = ((By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/div[2]/table/thead/tr/th[2]/div'))
    firstEditorLink = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[7]/div/div/span[1]')
    firstRecordDeleteLink =(By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr[1]/td[7]/div/div/span[2]')
    firstRecordRadioBox = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr[1]/td[1]/div/label/span/span')
    delSuccessToast = (By.CSS_SELECTOR, 'body > div.el-message.el-message--success > p')
    addCameraSuccessTost = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')
    edtSuccessToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')


    def query_video(self,ipOrName):
        query = self.driver.find_element(*VideoManagerPage.queryInputBox)
        query.send_keys(ipOrName)

    def click_manualAddButton(self):
        manualAddButton = self.driver.find_element(*VideoManagerPage.manualAddButton)
        self.driver.execute_script("arguments[0].click();", manualAddButton)

    def get_manualAddButton(self):
        text = self.driver.find_element(*VideoManagerPage.manualAddButton).text
        return text

    def click_batchDeleteButton(self):
        batchDeleteButton = self.driver.find_element(*VideoManagerPage.batchDeleteButton)
        self.driver.execute_script("arguments[0].click();", batchDeleteButton)

    def click_batchDeleteRadio(self):
        batchDeleteRadio = self.driver.find_element(*VideoManagerPage.batchDeleteRadio)
        self.driver.execute_script("arguments[0].click();", batchDeleteRadio)

    def click_batchDeleteConfirmButton(self):
        batchDeleteConfirmButton = self.driver.find_element(*VideoManagerPage.batchDeleteConfirmButton)
        self.driver.execute_script("arguments[0].click();", batchDeleteConfirmButton)

    def get_videoAccessEml(self):
        text = self.driver.find_element(*VideoManagerPage.videoAccessEml).text
        return text

    def get_deviceTypeEml(self):
        text = self.driver.find_element(*VideoManagerPage.deviceTypeEml).text
        return text

    def click_firstRecordDeleteLink(self):
        firstRecordDeleteLink = self.driver.find_element(*VideoManagerPage.firstRecordDeleteLink)
        self.driver.execute_script("arguments[0].click();", firstRecordDeleteLink)
        confirmButt = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-message.delVideoContainer > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span')
        confirmButtEml = self.driver.find_element(*confirmButt)
        self.driver.execute_script("arguments[0].click();", confirmButtEml)

    def click_firstEditorLink(self):
        firstEditorLink = self.driver.find_element(*VideoManagerPage.firstEditorLink)
        self.driver.execute_script("arguments[0].click();", firstEditorLink)

    def click_firstRecordRadioBox(self):
        firstRecordRadioBox = self.driver.find_element(*VideoManagerPage.firstRecordRadioBox)
        self.driver.execute_script("arguments[0].click();", firstRecordRadioBox)

    def get_delSuccessToast(self):
         return self.driver.find_element(*VideoManagerPage.delSuccessToast).text

    def get_addCameraSuccessTost(self):
         return self.driver.find_element(*VideoManagerPage.addCameraSuccessTost).text

    def get_edtSuccessToast(self):
        return self.driver.find_element(*VideoManagerPage.edtSuccessToast).text

    def get_video_list(self):
        arr=[]
        videoList = []
        table_loc = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/div[3]/table/tbody')
        try:
            table_tr_list = self.driver.find_element(*table_loc).find_elements(By.TAG_NAME,'tr')
        except Exception as e:
            return videoList
        else:
            if len(table_tr_list)>0:
                for tr in table_tr_list:
                    arr1 = (tr.text).split(' ')
                    # print(arr1)
                    arr.append(arr1)
                for i in range(len(arr)):
                    li = []
                    for j in range(len(arr[i])):
                        arr1 = arr[i][j].split('\n')
                        li = li +arr1
                    videoList.append(li)
        return videoList


    class IpStreamAdd(BasePage):
        ipAddrAdd = (By.XPATH,'//*[@id="tab-first"]')
        cameraType = (By.XPATH,'//*[@id="pane-first"]/form/div[1]/div/div/div/input')
        seemartCameraType = (By.XPATH,'/html/body/div[4]/div[1]/div[1]/ul/li[1]/span')
        cameraIpBox = (By.XPATH,'//*[@id="pane-first"]/form/div[2]/div/div[1]/input')
        userNameBox = (By.XPATH,'//*[@id="pane-first"]/form/div[3]/div/div/input')
        pwdBox = (By.XPATH, '//*[@id="pane-first"]/form/div[4]/div/div/input')

        ordinaryCameraType = (By.XPATH,'//span[text()="普通摄像机"]')
        rtstStreamBox = (By.XPATH,'//*[@id="pane-first"]/form/div[2]/div/div/input')
        userNameoBox = (By.XPATH,'//*[@id="pane-first"]/form/div[3]/div/div/input')
        pwdoBox = (By.XPATH, '//*[@id="pane-first"]/form/div[4]/div/div/input')

        ipAddrMultAdd = (By.XPATH, '//*[@id="tab-second"]')
        mulCameraType = (By.XPATH,'//*[@id="pane-second"]/form/div[1]/div/div/div/input')
        seemartCameraMultType = (By.XPATH, '/html/body/div[4]/div[1]/div[1]/ul/li[1]/span')
        cameraStartIpMultBox = (By.XPATH, '//*[@id="pane-second"]/form/div[2]/div/div/input')
        cameraEndIpMultBox = (By.XPATH, '//*[@id="pane-second"]/form/div[3]/div/div/input')
        userNameMultBox = (By.XPATH, '//*[@id="pane-second"]/form/div[4]/div/div/input')
        pwdMultBox = (By.XPATH, '//*[@id="pane-second"]/form/div[5]/div/div/input')

        ordinaryCameraMultType = (By.CSS_SELECTOR, 'body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > ul > li:nth-child(2)')
        rtstStreamStartBox = (By.XPATH, '//*[@id="pane-second"]/form/div[2]/div/div/input')
        rtstStreamEndBox = (By.XPATH, '//*[@id="pane-second"]/form/div[3]/div/div/input')
        userNameoMultBox = (By.XPATH, '//*[@id="pane-second"]/form/div[4]/div/div/input')
        pwdoMultBox = (By.XPATH, '//*[@id="pane-second"]/form/div[5]/div/div/input')

        edtNameBox = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-dialog.editVideo > div > div.el-dialog__body > div > div > form > div:nth-child(3) > div > div > input')
        edtRemarkBox = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-dialog.editVideo > div > div.el-dialog__body > div > div > form > div.el-form-item.remarks > div > div > textarea')
        edtOptimalCaptureRadio = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-dialog.editVideo > div > div.el-dialog__body > div > div > form > div.el-form-item.setting > div > div > label.el-radio.is-checked > span.el-radio__input.is-checked > span')
        edtFastCaptureRadio = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-dialog.editVideo > div > div.el-dialog__body > div > div > form > div.el-form-item.setting > div > div > label:nth-child(1) > span.el-radio__input > span')
        edtCancelButton = (By.CSS_SELECTOR,
                        'body > div.el-dialog__wrapper.xg-dialog.editVideo > div > div.el-dialog__footer > div > button.el-button.btn.el-button--default > span')
        edtConfirmButton = (By.CSS_SELECTOR,
                         'body > div.el-dialog__wrapper.xg-dialog.editVideo > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span')

        cancelButton = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-dialog.addVideo > div > div.el-dialog__footer > div > button.el-button.btn.el-button--default > span')
        confirmButton = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-dialog.addVideo > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span')

        def click_ipAddrAdd(self):
            ipAddrAdd = self.driver.find_element(*VideoManagerPage.IpStreamAdd.ipAddrAdd)
            self.driver.execute_script("arguments[0].click();", ipAddrAdd)

        def click_cameraType(self):
            cameraType = self.driver.find_element(*VideoManagerPage.IpStreamAdd.cameraType)
            self.driver.execute_script("arguments[0].click();", cameraType)

        def select_seemartCameraType(self):
            seemartCameraType = self.driver.find_element(*VideoManagerPage.IpStreamAdd.seemartCameraType)
            self.driver.execute_script("arguments[0].click();", seemartCameraType)

        def select_ordinaryCameraType(self):
            ordinaryCameraType = self.driver.find_element(*VideoManagerPage.IpStreamAdd.ordinaryCameraType)
            self.driver.execute_script("arguments[0].click();", ordinaryCameraType)

        def set_cameraIpBox(self,ip):
            cameraIp = self.driver.find_element(*VideoManagerPage.IpStreamAdd.cameraIpBox)
            cameraIp.send_keys(ip)

        def set_userName(self,name):
            userName = self.driver.find_element(*VideoManagerPage.IpStreamAdd.userNameoBox)
            userName.send_keys(name)

        def set_userpwd(self,pwd):
            pwdBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.pwdBox)
            pwdBox.send_keys(pwd)

        def click_ipAddrMultAdd(self):
            ipAddrMultAdd = self.driver.find_element(*VideoManagerPage.IpStreamAdd.ipAddrMultAdd)
            self.driver.execute_script("arguments[0].click();", ipAddrMultAdd)

        def click_mulCameraType(self):
            mulCameraType = self.driver.find_element(*VideoManagerPage.IpStreamAdd.mulCameraType)
            self.driver.execute_script("arguments[0].click();", mulCameraType)

        def click_seemartCameraMultType(self):
            seemartCameraMultType = self.driver.find_element(*VideoManagerPage.IpStreamAdd.seemartCameraMultType)
            self.driver.execute_script("arguments[0].click();", seemartCameraMultType)

        def set_cameraStartIpMultBox(self,ip):
            cameraStartIpMultBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.cameraStartIpMultBox)
            cameraStartIpMultBox.send_keys(ip)

        def set_cameraEndIpMultBox(self,ip):
            cameraEndIpMultBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.cameraEndIpMultBox)
            cameraEndIpMultBox.send_keys(ip)

        def set_userNameMultBox(self,username):
            userNameMultBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.userNameMultBox)
            userNameMultBox.send_keys(username)

        def set_pwdMultBox(self,pwd):
            pwdMultBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.pwdMultBox)
            pwdMultBox.send_keys(pwd)

        def select_ordinaryCameraMultType(self):
            ordinaryCameraMultType = self.driver.find_element(*VideoManagerPage.IpStreamAdd.ordinaryCameraMultType)
            self.driver.execute_script("arguments[0].click();", ordinaryCameraMultType)

        def set_rtstStreamStartBox(self,rtsp):
            rtstStreamStartBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.rtstStreamStartBox)
            rtstStreamStartBox.send_keys(rtsp)

        def set_rtstStreamEndBox(self,rtsp):
            rtstStreamEndBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.rtstStreamEndBox)
            rtstStreamEndBox.send_keys(rtsp)

        def set_userNameoMultBox(self,username):
            userNameoMultBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.userNameoMultBox)
            userNameoMultBox.send_keys(username)

        def set_pwdoMultBox(self,pwd):
            pwdoMultBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.pwdoMultBox)
            pwdoMultBox.send_keys(pwd)

        def set_edtNameBox(self,name):
            edtNameBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.edtNameBox)
            edtNameBox.send_keys(name)

        def set_edtRemarkBox(self,remark):
            edtRemarkBox = self.driver.find_element(*VideoManagerPage.IpStreamAdd.edtRemarkBox)
            edtRemarkBox.send_keys(remark)

        def click_cancelButton(self):
            cancelButton = self.driver.find_element(*VideoManagerPage.IpStreamAdd.cancelButton)
            self.driver.execute_script("arguments[0].click();", cancelButton)

        def click_edtFastCaptureRadio(self):
            edtFastCaptureRadio = self.driver.find_element(*VideoManagerPage.IpStreamAdd.edtFastCaptureRadio)
            self.driver.execute_script("arguments[0].click();", edtFastCaptureRadio)

        def click_edtOptimalCaptureRadio(self):
            edtOptimalCaptureRadio = self.driver.find_element(*VideoManagerPage.IpStreamAdd.edtOptimalCaptureRadio)
            self.driver.execute_script("arguments[0].click();", edtOptimalCaptureRadio)

        def click_confirmButton(self):
            confirmButton = self.driver.find_element(*VideoManagerPage.IpStreamAdd.confirmButton)
            self.driver.execute_script("arguments[0].click();", confirmButton)

        def click_edtConfirmButton(self):
            edtConfirmButton = self.driver.find_element(*VideoManagerPage.IpStreamAdd.edtConfirmButton)
            self.driver.execute_script("arguments[0].click();", edtConfirmButton)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    base_url = cc.baseUrl()
    driver.get(base_url)
    loginPage = LoginPage(driver)
    driver.implicitly_wait(30)
    loginPage.set_username('admin')
    loginPage.set_password('123456')
    time.sleep(1)
    loginPage.click_SignIn()
    time.sleep(2)

    homepage = HomePage(driver)
    homepage.click_mainMenuButton()
    time.sleep(2)

    videoManPage = VideoManagerPage(driver)
    videoManPage.click_manualAddButton()
    time.sleep(2)
    ipStreamPage = VideoManagerPage.IpStreamAdd(driver)
    ipStreamPage.click_ipAddrMultAdd()
    time.sleep(1)
    ipStreamPage.click_mulCameraType()
    time.sleep(0.5)
    ipStreamPage.select_ordinaryCameraMultType()
    ipStreamPage.set_rtstStreamStartBox('rtsp://10.58.133.10')
    ipStreamPage.set_rtstStreamEndBox('rtsp://10.58.133.13')
    ipStreamPage.set_userNameoMultBox('admin')
    ipStreamPage.set_pwdoMultBox('123456')
    ipStreamPage.click_confirmButton()
