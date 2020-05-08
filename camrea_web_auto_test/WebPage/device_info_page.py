#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   device_info_page.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 17:10   xushaohua      1.0         None
'''

from selenium.webdriver.common.by import By
from WebPage.base_page import BasePage

class DeviceInfoPage(BasePage):
    # page element identifier
    deviceNameField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/span[2]')
    deviceTypeField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/span[2]')
    serialNumberField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[3]/span[2]')
    macAddressField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[4]/span[2]')
    hardwareVersionField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[5]/span[2]')
    softwareVersionField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[6]/span[2]')

    def get_deviceNameField(self):
        deviceName = self.driver.find_element(*DeviceInfoPage.deviceNameField).text
        return deviceName

    def get_deviceTypeField(self):
        deviceType = self.driver.find_element(*DeviceInfoPage.deviceTypeField).text
        return deviceType

    def get_serialNumberField(self):
        serialNumber = self.driver.find_element(*DeviceInfoPage.serialNumberField).text
        return serialNumber

    def get_macAddressField(self):
        macAddress = self.driver.find_element(*DeviceInfoPage.macAddressField).text
        return macAddress

    def get_hardwareVersionField(self):
        hardwareVersion = self.driver.find_element(*DeviceInfoPage.hardwareVersionField).text
        return hardwareVersion

    def get_softwareVersionField(self):
        softwareVersion = self.driver.find_element(*DeviceInfoPage.softwareVersionField).text
        return softwareVersion