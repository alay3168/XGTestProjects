#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   capture_protocol_page.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 17:08   xushaohua      1.0         None
'''

from selenium.webdriver.common.by import By
from WebPage.base_page import BasePage
from selenium.webdriver.common.keys import Keys

class CaptureProtocolPage(BasePage):
    # page element identifier
    puppyTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/label[1]/span[2]')
    puppyServerIPField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[1]/div/div/input')
    puppyPortField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[2]/div/div/input')
    puppyConnectionStatus = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[3]/div/span')
    puppySaveButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[4]/div/button/span')
    saveSuccessToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')
    puppyServerIPErrToast = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.trans-puppy > form > div:nth-child(1) > div > div.el-form-item__error')
    puppyPortErrToast = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.trans-puppy > form > div:nth-child(2) > div > div.el-form-item__error')


    FTPTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/label[2]/span[2]')
    ftpServerIPField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[1]/div/div/input')
    ftpPortField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[2]/div/div/input')
    ftpUserNameField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[3]/div/div/input')
    ftpPasswdField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[4]/div/div/input')
    ftpPictureArchivingLower = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[5]/div/div/span[1]')
    ftpPictureArchivingUp = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[5]/div/div/span[2]')
    ftpUploadTestPicturesButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[5]/div/button/span')
    ftpSaveRootDirTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[6]/div/div/label[1]')
    ftpSaveOneLevelTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[6]/div/div/label[2]')
    ftpSaveButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[7]/div/button')

    ftpUploadTestPictureToast = (By.XPATH,'/html/body/div[2]/p')
    ftpServerIPErrToast = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.trans-ftp > form > div.el-form-item.is-error.is-no-asterisk > div > div.el-form-item__error')
    ftpPortErrToast = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.trans-ftp > form > div.el-form-item.is-error.is-no-asterisk > div > div.el-form-item__error')
    ftpUserNameErrToast = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.trans-ftp > form > div.el-form-item.is-error.is-no-asterisk > div > div.el-form-item__error')
    ftpPasswdErrToast = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > div.trans-ftp > form > div.el-form-item.is-error.is-no-asterisk > div > div.el-form-item__error')

    def select_puppyTab(self):
        puppyTab = self.driver.find_element(*CaptureProtocolPage.puppyTab)
        self.driver.execute_script("arguments[0].click();", puppyTab)

    def set_puppyServerIPField(self,serverIp):
        puppyServerIPField = self.driver.find_element(*CaptureProtocolPage.puppyServerIPField)
        puppyServerIPField.send_keys(serverIp)

    def clear_puppyServerIPField(self):
        eml = self.driver.find_element(*CaptureProtocolPage.puppyServerIPField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def set_puppyPortField(self,port):
        puppyPortField = self.driver.find_element(*CaptureProtocolPage.puppyPortField)
        puppyPortField.send_keys(port)


    def clear_puppyPortField(self):
        eml = self.driver.find_element(*CaptureProtocolPage.puppyPortField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def check_puppyConnectionStatus(self):
        puppyConnectionStatus = self.driver.find_element(*CaptureProtocolPage.puppyConnectionStatus)
        puppyConnectionStatus.isEnabled()

    def click_puppySaveButton(self):
        puppySaveButton = self.driver.find_element(*CaptureProtocolPage.puppySaveButton)
        self.driver.execute_script("arguments[0].click();", puppySaveButton)

    def get_saveSuccessToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.saveSuccessToast).text
        return text

    def get_ftpUploadTestPictureToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.ftpUploadTestPictureToast).text
        return text

    def get_puppyServerIPErrToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.puppyServerIPErrToast).text
        return text

    def get_puppyPortErrToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.puppyPortErrToast).text
        return text

    def select_FTPTab(self):
        FTPTab = self.driver.find_element(*CaptureProtocolPage.FTPTab)
        self.driver.execute_script("arguments[0].click();", FTPTab)

    def set_ftpServerIPField(self,serverIp):
        ftpServerIPField = self.driver.find_element(*CaptureProtocolPage.ftpServerIPField)
        ftpServerIPField.send_keys(serverIp)

    def clear_ftpServerIPField(self):
        eml = self.driver.find_element(*CaptureProtocolPage.ftpServerIPField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def get_ftpServerIPErrToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.ftpServerIPErrToast).text
        return text

    def set_ftpPortField(self,port):
        ftpPortField = self.driver.find_element(*CaptureProtocolPage.ftpPortField)
        ftpPortField.send_keys(port)

    def clear_ftpPortField(self):
        eml = self.driver.find_element(*CaptureProtocolPage.ftpPortField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def get_ftpPortErrToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.ftpPortErrToast).text
        return text

    def set_ftpUserNameField(self,ftpUserName):
        ftpUserNameField = self.driver.find_element(*CaptureProtocolPage.ftpUserNameField)
        ftpUserNameField.send_keys(ftpUserName)

    def clear_ftpUserNameField(self):
        eml = self.driver.find_element(*CaptureProtocolPage.ftpUserNameField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def get_ftpUserNameErrToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.ftpUserNameErrToast).text
        return text

    def set_ftpPasswdField(self,ftpPasswd):
        ftpPasswdField = self.driver.find_element(*CaptureProtocolPage.ftpPasswdField)
        ftpPasswdField.send_keys(ftpPasswd)

    def clear_ftpPasswdField(self):
        eml = self.driver.find_element(*CaptureProtocolPage.ftpPasswdField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def get_fftpPasswdErrToast(self):
        text = self.driver.find_element(*CaptureProtocolPage.ftpPasswdErrToast).text
        return text

    def set_ftpPictureArchivingLower(self):
        ftpPictureArchivingLower = self.driver.find_element(*CaptureProtocolPage.ftpPictureArchivingLower)
        self.driver.execute_script("arguments[0].click();", ftpPictureArchivingLower)

    def set_ftpPictureArchivingUp(self):
        ftpPictureArchivingUp = self.driver.find_element(*CaptureProtocolPage.ftpPictureArchivingUp)
        self.driver.execute_script("arguments[0].click();", ftpPictureArchivingUp)

    def click_ftpUploadTestPicturesButton(self):
        ftpUploadTestPicturesButton = self.driver.find_element(*CaptureProtocolPage.ftpUploadTestPicturesButton)
        self.driver.execute_script("arguments[0].click();", ftpUploadTestPicturesButton)

    def select_ftpSaveRootDirTab(self):
        ftpSaveRootDirTab = self.driver.find_element(*CaptureProtocolPage.ftpSaveRootDirTab)
        self.driver.execute_script("arguments[0].click();", ftpSaveRootDirTab)

    def select_ftpSaveOneLevelTab(self):
        ftpSaveOneLevelTab = self.driver.find_element(*CaptureProtocolPage.ftpSaveOneLevelTab)
        self.driver.execute_script("arguments[0].click();", ftpSaveOneLevelTab)

    def click_ftpSaveButton(self):
        ftpSaveButton = self.driver.find_element(*CaptureProtocolPage.ftpSaveButton)
        self.driver.execute_script("arguments[0].click();", ftpSaveButton)