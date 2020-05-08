#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tcpip_page.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 17:08   xushaohua      1.0         None
'''

from selenium.webdriver.common.by import By
from WebPage.base_page import BasePage
from selenium.webdriver.common.keys import Keys

class TcpIpPage(BasePage):

    autoIpAddrTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[1]/div/div/label[1]/span[2]')
    manualIpAddrTab = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[1]/div/div/label[2]/span[2]')

    ipV4AddrField = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > form > div:nth-child(2) > div > div > input')
    ipV4AddrNullMessage = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[2]/div/div[2]')
    ipV4AddrErrMessage = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[2]/div/div[2]')
    subnetMaskField = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > form > div:nth-child(3) > div > div > input')
    subnetMaskNullMessage = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[3]/div/div[2]')
    subnetMaskErrMessage = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[3]/div/div[2]')
    defaultGatewayField = (By.CSS_SELECTOR,'#app > div > div > section > div > div.app-main > section > div > form > div:nth-child(4) > div > div > input')
    defaultGatewayNullMessage = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[4]/div/div[2]')
    defaultGatewayErrMessage = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[4]/div/div[2]')
    firstDNSField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[5]/div/div/input')
    firstDNSNullMessage = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[5]/div/div[2]')
    firstDNSErrMessage = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[5]/div/div[2]')
    backDNSField = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[6]/div/div/input')
    backDNSErrMessage = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[6]/div/div[2]')

    saveButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/form/div[7]/div/button/span')
    saveSuccessToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')

    def select_autoIpAddrTab(self):
        autoIpAddrTab = self.driver.find_element(*TcpIpPage.autoIpAddrTab)
        self.driver.execute_script("arguments[0].click();", autoIpAddrTab)

    def select_manualIpAddrTab(self):
        manualIpAddrTab = self.driver.find_element(*TcpIpPage.manualIpAddrTab)
        self.driver.execute_script("arguments[0].click();", manualIpAddrTab)

    def clear_ipV4AddrField(self):
        ipV4AddrField = self.driver.find_element(*TcpIpPage.ipV4AddrField)
        ipV4AddrField.send_keys(Keys.CONTROL + 'a')
        ipV4AddrField.send_keys(Keys.DELETE)

    def click_ipV4AddrField(self):
        ipV4AddrField = self.driver.find_element(*TcpIpPage.ipV4AddrField)
        self.driver.execute_script("arguments[0].click();", ipV4AddrField)

    def set_ipV4AddrField(self,ip):
        ipV4AddrField = self.driver.find_element(*TcpIpPage.ipV4AddrField)
        ipV4AddrField.send_keys(ip)

    def get_ipV4AddrNullMessage(self):
        text = self.driver.find_element(*TcpIpPage.ipV4AddrNullMessage).text
        return text

    def get_ipV4AddrErrMessage(self):
        text = self.driver.find_element(*TcpIpPage.ipV4AddrErrMessage).text
        return text

    def clear_subnetMaskField(self):
        subnetMaskField = self.driver.find_element(*TcpIpPage.subnetMaskField)
        subnetMaskField.send_keys(Keys.CONTROL + 'a')
        subnetMaskField.send_keys(Keys.DELETE)

    def set_subnetMaskField(self,subnetMask):
        subnetMaskField = self.driver.find_element(*TcpIpPage.subnetMaskField)
        subnetMaskField.send_keys(subnetMask)

    def get_subnetMaskNullMessage(self):
        text = self.driver.find_element(*TcpIpPage.subnetMaskNullMessage).text
        return text

    def get_subnetMaskErrMessage(self):
        text = self.driver.find_element(*TcpIpPage.subnetMaskErrMessage).text
        return text

    def clear_defaultGatewayField(self):
        defaultGatewayField = self.driver.find_element(*TcpIpPage.defaultGatewayField)
        defaultGatewayField.send_keys(Keys.CONTROL + 'a')
        defaultGatewayField.send_keys(Keys.DELETE)

    def set_defaultGatewayField(self,defGateway):
        defaultGatewayField = self.driver.find_element(*TcpIpPage.defaultGatewayField)
        defaultGatewayField.send_keys(defGateway)

    def get_defaultGatewayNullMessage(self):
        text = self.driver.find_element(*TcpIpPage.defaultGatewayNullMessage).text
        return text

    def get_defaultGatewayErrMessage(self):
        text = self.driver.find_element(*TcpIpPage.defaultGatewayErrMessage).text
        return text

    def clear_firstDNSField(self):
        firstDNSField = self.driver.find_element(*TcpIpPage.firstDNSField)
        firstDNSField.send_keys(Keys.CONTROL + 'a')
        firstDNSField.send_keys(Keys.DELETE)

    def set_firstDNSField(self,dns):
        firstDNSField = self.driver.find_element(*TcpIpPage.firstDNSField)
        firstDNSField.send_keys(dns)

    def get_firstDNSNullMessage(self):
        text = self.driver.find_element(*TcpIpPage.firstDNSNullMessage).text
        return text

    def get_firstDNSErrMessage(self):
        text = self.driver.find_element(*TcpIpPage.firstDNSErrMessage).text
        return text

    def clear_backDNSField(self):
        backDNSField = self.driver.find_element(*TcpIpPage.backDNSField)
        backDNSField.send_keys(Keys.CONTROL + 'a')
        backDNSField.send_keys(Keys.DELETE)

    def set_backDNSField(self,dns):
        backDNSField = self.driver.find_element(*TcpIpPage.backDNSField)
        backDNSField.send_keys(dns)

    def get_backDNSErrMessage(self):
        text = self.driver.find_element(*TcpIpPage.backDNSErrMessage).text
        return text

    def click_saveButton(self):
        saveButton = self.driver.find_element(*TcpIpPage.saveButton)
        self.driver.execute_script("arguments[0].click();", saveButton)

    def get_saveSuccessToast(self):
        text = self.driver.find_element(*TcpIpPage.saveSuccessToast).text
        return text