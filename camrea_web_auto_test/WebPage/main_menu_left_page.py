#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main_menu_left_page.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 16:32   xushaohua      1.0         None
'''
from WebPage.base_page import BasePage
from selenium.webdriver.common.by import By


class MainMenuLeftPage(BasePage):
    # page element identifier
    videoManageMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[1]/li/div/span')
    videoAccessMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[1]/li/ul/a/li/span')

    networkProtocolMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[2]/li/div/span')
    tcpIpMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[2]/li/ul/a[1]/li/span')
    captureProtocolMenu = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[2]/li/ul/a[2]/li/span')

    intelligentManageMenu = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[3]/li/div/span')
    faceMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[3]/li/ul/a/li/span')

    userManageMenu = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[4]/li/div/span')
    userMenu = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[4]/li/ul/a/li/span')

    systemManageMenu = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[5]/li/div/span')
    deviceInfoMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[5]/li/ul/a[1]/li/span')
    timeSetMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[5]/li/ul/a[2]/li/span')

    localMenu = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[6]/li/div/span')
    systemMaintenanceMenu = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[1]/div[1]/div/ul/div[6]/li/ul/a/li/span')

    def click_videoManageMenu(self):
        videoManageMenu = self.driver.find_element(*MainMenuLeftPage.videoManageMenu)
        self.driver.execute_script("arguments[0].click();", videoManageMenu)

    def click_videoAccessMenu(self):
        videoAccessMenu = self.driver.find_element(*MainMenuLeftPage.videoAccessMenu)
        self.driver.execute_script("arguments[0].click();", videoAccessMenu)

    def click_networkProtocolMenu(self):
        networkProtocolMenu = self.driver.find_element(*MainMenuLeftPage.networkProtocolMenu)
        self.driver.execute_script("arguments[0].click();", networkProtocolMenu)

    def click_tcpIpMenu(self):
        tcpIpMenu = self.driver.find_element(*MainMenuLeftPage.tcpIpMenu)
        self.driver.execute_script("arguments[0].click();", tcpIpMenu)

    def click_captureProtocolMenu(self):
        captureProtocolMenu = self.driver.find_element(*MainMenuLeftPage.captureProtocolMenu)
        self.driver.execute_script("arguments[0].click();", captureProtocolMenu)

    def click_intelligentManageMenu(self):
        intelligentManageMenu = self.driver.find_element(*MainMenuLeftPage.intelligentManageMenu)
        self.driver.execute_script("arguments[0].click();", intelligentManageMenu)

    def click_faceMenu(self):
        faceMenu = self.driver.find_element(*MainMenuLeftPage.faceMenu)
        self.driver.execute_script("arguments[0].click();", faceMenu)

    def click_userManageMenu(self):
        userManageMenu = self.driver.find_element(*MainMenuLeftPage.userManageMenu)
        self.driver.execute_script("arguments[0].click();", userManageMenu)

    def click_userMenu(self):
        userMenu = self.driver.find_element(*MainMenuLeftPage.userMenu)
        self.driver.execute_script("arguments[0].click();", userMenu)

    def click_systemManageMenu(self):
        systemManageMenu = self.driver.find_element(*MainMenuLeftPage.systemManageMenu)
        self.driver.execute_script("arguments[0].click();", systemManageMenu)

    def click_deviceInfoMenu(self):
        deviceInfoMenu = self.driver.find_element(*MainMenuLeftPage.deviceInfoMenu)
        self.driver.execute_script("arguments[0].click();", deviceInfoMenu)

    def click_timeSetMenu(self):
        timeSetMenu = self.driver.find_element(*MainMenuLeftPage.timeSetMenu)
        self.driver.execute_script("arguments[0].click();", timeSetMenu)

    def click_localMenu(self):
        localMenu = self.driver.find_element(*MainMenuLeftPage.localMenu)
        self.driver.execute_script("arguments[0].click();", localMenu)

    def click_systemMaintenanceMenu(self):
        systemMaintenanceMenu = self.driver.find_element(*MainMenuLeftPage.systemMaintenanceMenu)
        self.driver.execute_script("arguments[0].click();", systemMaintenanceMenu)