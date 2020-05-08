#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   time_config_page.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 17:10   xushaohua      1.0         None
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from WebPage.base_page import BasePage

class TimeConfigPage(BasePage):

    timezoneDownBox = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[1]/div/div/div/input')
    timezoneDownBoxSub = (By.XPATH,'/html/body/div[2]/div[1]/div[1]/ul/li[28]/span')

    mannualSetTimeTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[2]/div/label/span[2]')
    deviceTimeField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[3]/div/div/input')
    setTimeField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[4]/div/div/input')
    syncWithComputerTime = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[4]/div/label/span[2]')

    ntpSetTimeTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[5]/div/label/span[2]')
    serverIpAddrField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[6]/div/div/input')
    ntpPortField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[7]/div/div/input')
    testPortButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[7]/div/button')
    timeIntervalField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[8]/div/div/input')
    serverIpAddrErrToast = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[6]/div/div[2]')
    ntpPortErrToast = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[7]/div/div[2]')
    timeIntervalErrToast = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[8]/div/div[2]')

    saveButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[9]/div/button')
    saveSuccessToast = (By.CSS_SELECTOR, 'body > div.el-message.el-message--success > p')
    testPortErrToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--error > p')
    # testPortSuccessToast = (By.CSS_SELECTOR,'body > div:nth-child(8) > p')


    def click_timezoneDownBox(self):
        eml = self.driver.find_element(*TimeConfigPage.timezoneDownBox)
        self.driver.execute_script("arguments[0].click();", eml)

    def select_timezoneDownBoxSub(self):
        sub = self.driver.find_element(*TimeConfigPage.timezoneDownBoxSub)
        self.driver.execute_script("arguments[0].click();", sub)

    def select_mannualSetTimeTab(self):
        mannualSetTimeTab = self.driver.find_element(*TimeConfigPage.mannualSetTimeTab)
        self.driver.execute_script("arguments[0].click();", mannualSetTimeTab)

    def get_deviceTimeField(self):
        deviceTimeField = self.driver.find_element(*TimeConfigPage.deviceTimeField)
        self.driver.execute_script("arguments[0].click();", deviceTimeField)

    def clear_setTimeField(self):
        setTimeField = self.driver.find_element(*TimeConfigPage.setTimeField)
        setTimeField.clear()

    def set_setTimeField(self,time):
        setTimeField = self.driver.find_element(*TimeConfigPage.setTimeField)
        setTimeField.send_keys(time)

    def select_syncWithComputerTime(self):
        syncWithComputerTime = self.driver.find_element(*TimeConfigPage.syncWithComputerTime)
        self.driver.execute_script("arguments[0].click();", syncWithComputerTime)

    def select_ntpSetTimeTab(self):
        ntpSetTimeTab = self.driver.find_element(*TimeConfigPage.ntpSetTimeTab)
        self.driver.execute_script("arguments[0].click();", ntpSetTimeTab)

    def clear_serverIpAddrField(self):
        eml = self.driver.find_element(*TimeConfigPage.serverIpAddrField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def set_serverIpAddrField(self,ip):
        serverIpAddrField = self.driver.find_element(*TimeConfigPage.serverIpAddrField)
        serverIpAddrField.send_keys(ip)

    def clear_ntpPortField(self):
        eml = self.driver.find_element(*TimeConfigPage.ntpPortField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def set_ntpPortField(self, port):
        ntpPortField = self.driver.find_element(*TimeConfigPage.ntpPortField)
        ntpPortField.send_keys(port)

    def click_testPortButton(self):
        testPortButton = self.driver.find_element(*TimeConfigPage.testPortButton)
        self.driver.execute_script("arguments[0].click();", testPortButton)

    def clear_timeIntervalField(self):
        eml = self.driver.find_element(*TimeConfigPage.timeIntervalField)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)

    def set_timeIntervalField(self, number):
        timeIntervalField = self.driver.find_element(*TimeConfigPage.timeIntervalField)
        timeIntervalField.send_keys(number)

    def click_saveButton(self):
        saveButton = self.driver.find_element(*TimeConfigPage.saveButton)
        self.driver.execute_script("arguments[0].click();", saveButton)

    def get_saveSuccessToast(self):
        text = self.driver.find_element(*TimeConfigPage.saveSuccessToast).text
        return text

    def get_serverIpAddrErrToast(self):
        text = self.driver.find_element(*TimeConfigPage.serverIpAddrErrToast).text
        return text

    def get_ntpPortErrToast(self):
        text = self.driver.find_element(*TimeConfigPage.ntpPortErrToast).text
        return text

    def get_timeIntervalErrToast(self):
        text = self.driver.find_element(*TimeConfigPage.timeIntervalErrToast).text
        return text

    def get_testPortSuccessToast(self):
        text = self.driver.find_element(*TimeConfigPage.testPortSuccessToast).text
        return text

    def get_testPortErrToast(self):
        text = self.driver.find_element(*TimeConfigPage.testPortErrToast).text
        return text

