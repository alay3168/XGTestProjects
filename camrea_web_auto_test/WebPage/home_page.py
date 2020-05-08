#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   home_page.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/23 10:31   xushaohua      1.0         None
'''
from WebPage.base_page import BasePage
from WebPage.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

class HomePage(BasePage):
    # page element identifier
    previewButton = (By.XPATH,'//*[@id="app"]/div/div/div/div[2]/ul/li[1]')
    mainMenuButton = (By.XPATH,'//*[@id="app"]/div/div/div/div[2]/ul/li[2]')
    userNameButton = (By.XPATH,'//*[@id="app"]/div/div/div/div[2]/ul/div/span/span')
    logoutButton = (By.XPATH,"//li[contains(.,'退出登录')]")
    immediatelyAddButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div/div/div/p[3]/button/span')


    addCameraButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/div[1]/button/span')
    detailsButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[3]/div/div[1]/button')

    seemarCameratList = (By.XPATH,"//div[@id='app']/div/div/section/div/div/div/div/div[2]/div/div/div")
    ordinaryCameraList = (By.XPATH,"//div[@id='app']/div/div/section/div/div/div/div/div[2]/div[2]/div/div")

    monitorScreenEml = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[2]/div/div[1]/span')
    cameraListEml = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/div[1]/span')
    realTimeCaptureEml = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[3]/div/div[1]/span')

    addCameraSuccessTost = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')


    #operate page element
    def click_previewButton(self):
        cpbtn = self.driver.find_element(*HomePage.previewButton)
        self.driver.execute_script("arguments[0].click();", cpbtn)

    def get_previewButton(self):
        return self.driver.find_element(*HomePage.previewButton).text

    def click_mainMenuButton(self):
        cmmbtn = self.driver.find_element(*HomePage.mainMenuButton)
        self.driver.execute_script("arguments[0].click();", cmmbtn)

    def get_mainMenuButton(self):
        return self.driver.find_element(*HomePage.mainMenuButton).text

    def click_userNameButton(self):
        cunbtn = self.driver.find_element(*HomePage.userNameButton)
        self.driver.execute_script("arguments[0].click();", cunbtn)

    def get_userNameButton(self):
        return self.driver.find_element(*HomePage.userNameButton).text

    def click_logoutButton(self):
        clbtn = self.driver.find_element(*HomePage.logoutButton)

        self.driver.execute_script("arguments[0].click();", clbtn)

    def click_immediatelyAddButton(self):
        ciab = self.driver.find_element(*HomePage.immediatelyAddButton)
        self.driver.execute_script("arguments[0].click();", ciab)

    def get_immediatelyAddButton(self):
        text = self.driver.find_element(*HomePage.immediatelyAddButton).text
        return text

    def click_addCameraButton(self):
        cacbtn = self.driver.find_element(*HomePage.addCameraButton)
        self.driver.execute_script("arguments[0].click();", cacbtn)

    def get_addCameraButton(self):
        text = self.driver.find_element(*HomePage.addCameraButton).text
        return text

    def click_detailsButton(self):
        ccdcbtn = self.driver.find_element(*HomePage.detailsButton)
        self.driver.execute_script("arguments[0].click();", ccdcbtn)

    def get_detailsButton(self):
        text = self.driver.find_element(*HomePage.detailsButton).text
        return text

    def click_seemarCameratList(self):
        cscl = self.driver.find_element(*HomePage.seemarCameratList)
        self.driver.execute_script("arguments[0].click();", cscl)

    def get_seemarCameratList(self):
        text = self.driver.find_element(*HomePage.seemarCameratList).text
        return text

    def click_ordinaryCameraList(self):
        cocl = self.driver.find_element(*HomePage.ordinaryCameraList)
        self.driver.execute_script("arguments[0].click();", cocl)

    def get_ordinaryCameraList(self):
        text = self.driver.find_element(*HomePage.ordinaryCameraList).text
        return text

    def get_monitorScreenEml(self):
        text = self.driver.find_element(*HomePage.monitorScreenEml).text
        return text

    def get_cameraListEml(self):
        text = self.driver.find_element(*HomePage.cameraListEml).text
        return text

    def get_realTimeCaptureEml(self):
        text = self.driver.find_element(*HomePage.realTimeCaptureEml).text
        return text

    def get_addCameraSuccessTost(self):
         return self.driver.find_element(*HomePage.addCameraSuccessTost).text

    class IpStreamAdd(BasePage):
        ipAddrAdd = (By.XPATH,'//*[@id="tab-first"]')
        cameraType = (By.XPATH,'//*[@id="pane-first"]/form/div[1]/div/div/div[1]/input')
        seemartCameraType = (By.XPATH,'/html/body/div[4]/div[1]/div[1]/ul/li[1]/span')
        cameraIpBox = (By.XPATH,'//*[@id="pane-first"]/form/div[2]/div/div[1]/input')
        userNameBox = (By.XPATH,'//*[@id="pane-first"]/form/div[3]/div/div/input')
        pwdBox = (By.XPATH, '//*[@id="pane-first"]/form/div[4]/div/div/input')

        ordinaryCameraType = (By.XPATH,'/html/body/div[4]/div[1]/div[1]/ul/li[2]/span')
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

        ordinaryCameraMultType = (By.CSS_SELECTOR, 'body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child(2) > span')
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
            ipAddrAdd = self.driver.find_element(*HomePage.IpStreamAdd.ipAddrAdd)
            self.driver.execute_script("arguments[0].click();", ipAddrAdd)

        def click_cameraType(self):
            cameraType = self.driver.find_element(*HomePage.IpStreamAdd.cameraType)
            self.driver.execute_script("arguments[0].click();", cameraType)

        def select_seemartCameraType(self):
            seemartCameraType = self.driver.find_element(*HomePage.IpStreamAdd.seemartCameraType)
            self.driver.execute_script("arguments[0].click();", seemartCameraType)

        def select_ordinaryCameraType(self):
            ordinaryCameraType = self.driver.find_element(*HomePage.IpStreamAdd.ordinaryCameraType)
            self.driver.execute_script("arguments[0].click();", ordinaryCameraType)

        def set_cameraIpBox(self,ip):
            cameraIp = self.driver.find_element(*HomePage.IpStreamAdd.cameraIpBox)
            cameraIp.send_keys(ip)

        def set_userName(self,name):
            userName = self.driver.find_element(*HomePage.IpStreamAdd.userNameoBox)
            userName.send_keys(name)

        def set_userpwd(self,pwd):
            pwdBox = self.driver.find_element(*HomePage.IpStreamAdd.pwdBox)
            pwdBox.send_keys(pwd)

        def click_ipAddrMultAdd(self):
            ipAddrMultAdd = self.driver.find_element(*HomePage.IpStreamAdd.ipAddrMultAdd)
            self.driver.execute_script("arguments[0].click();", ipAddrMultAdd)

        def click_mulCameraType(self):
            mulCameraType = self.driver.find_element(*HomePage.IpStreamAdd.mulCameraType)
            self.driver.execute_script("arguments[0].click();", mulCameraType)

        def click_seemartCameraMultType(self):
            seemartCameraMultType = self.driver.find_element(*HomePage.IpStreamAdd.seemartCameraMultType)
            self.driver.execute_script("arguments[0].click();", seemartCameraMultType)

        def set_cameraStartIpMultBox(self,ip):
            cameraStartIpMultBox = self.driver.find_element(*HomePage.IpStreamAdd.cameraStartIpMultBox)
            cameraStartIpMultBox.send_keys(ip)

        def set_cameraEndIpMultBox(self,ip):
            cameraEndIpMultBox = self.driver.find_element(*HomePage.IpStreamAdd.cameraEndIpMultBox)
            cameraEndIpMultBox.send_keys(ip)

        def set_userNameMultBox(self,username):
            userNameMultBox = self.driver.find_element(*HomePage.IpStreamAdd.userNameMultBox)
            userNameMultBox.send_keys(username)

        def set_pwdMultBox(self,pwd):
            pwdMultBox = self.driver.find_element(*HomePage.IpStreamAdd.pwdMultBox)
            pwdMultBox.send_keys(pwd)

        def select_ordinaryCameraMultType(self):
            ordinaryCameraMultType = self.driver.find_element(*HomePage.IpStreamAdd.ordinaryCameraMultType)
            self.driver.execute_script("arguments[0].click();", ordinaryCameraMultType)

        def set_rtstStreamStartBox(self,rtsp):
            rtstStreamStartBox = self.driver.find_element(*HomePage.IpStreamAdd.rtstStreamStartBox)
            rtstStreamStartBox.send_keys(rtsp)

        def set_rtstStreamEndBox(self,rtsp):
            rtstStreamEndBox = self.driver.find_element(*HomePage.IpStreamAdd.rtstStreamEndBox)
            rtstStreamEndBox.send_keys(rtsp)

        def set_userNameoMultBox(self,username):
            userNameoMultBox = self.driver.find_element(*HomePage.IpStreamAdd.userNameoMultBox)
            userNameoMultBox.send_keys(username)

        def set_pwdoMultBox(self,pwd):
            pwdoMultBox = self.driver.find_element(*HomePage.IpStreamAdd.pwdoMultBox)
            pwdoMultBox.send_keys(pwd)

        def set_edtNameBox(self,name):
            edtNameBox = self.driver.find_element(*HomePage.IpStreamAdd.edtNameBox)
            edtNameBox.send_keys(name)

        def set_edtRemarkBox(self,remark):
            edtRemarkBox = self.driver.find_element(*HomePage.IpStreamAdd.edtRemarkBox)
            edtRemarkBox.send_keys(remark)

        def click_cancelButton(self):
            cancelButton = self.driver.find_element(*HomePage.IpStreamAdd.cancelButton)
            self.driver.execute_script("arguments[0].click();", cancelButton)

        def click_edtFastCaptureRadio(self):
            edtFastCaptureRadio = self.driver.find_element(*HomePage.IpStreamAdd.edtFastCaptureRadio)
            self.driver.execute_script("arguments[0].click();", edtFastCaptureRadio)

        def click_edtOptimalCaptureRadio(self):
            edtOptimalCaptureRadio = self.driver.find_element(*HomePage.IpStreamAdd.edtOptimalCaptureRadio)
            self.driver.execute_script("arguments[0].click();", edtOptimalCaptureRadio)

        def click_confirmButton(self):
            confirmButton = self.driver.find_element(*HomePage.IpStreamAdd.confirmButton)
            self.driver.execute_script("arguments[0].click();", confirmButton)

        def click_edtConfirmButton(self):
            edtConfirmButton = self.driver.find_element(*HomePage.IpStreamAdd.edtConfirmButton)
            self.driver.execute_script("arguments[0].click();", edtConfirmButton)

if __name__ == "__main__":

    driver = webdriver.Chrome()
    driver.set_window_size(1920,1080)
    LoginPage = LoginPage(driver)


    LoginPage.driver.get("http://10.58.122.108/")
    LoginPage.driver.implicitly_wait(30)

    LoginPage.set_username("admin")
    LoginPage.set_password("123456")
    LoginPage.click_SignIn()
    time.sleep(1)

    HomePage = HomePage(driver)
    # HomePage.click_seemarCameratList()
    # time.sleep(2)
    # HomePage.click_ordinaryCameraList()
    # time.sleep(2)
    HomePage.click_previewButton()
    time.sleep(2)
    print(HomePage.get_previewButton())
    # HomePage.click_mainMenuButton()
    print(HomePage.get_mainMenuButton())
    time.sleep(2)
    # HomePage.click_userNameButton()
    time.sleep(2)
    HomePage.click_logoutButton()
    time.sleep(2)
    driver.close()
