#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   system_maintenance_page.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 17:11   xushaohua      1.0         None
'''

from WebPage.base_page import BasePage
from selenium.webdriver.common.by import By

class SysMaintenancePage(BasePage):

    restartButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/div/button')
    restartconfirmButton = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-message > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span')
    restartToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--error > p')
    reFactorySetButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/div/button')
    exportParamentButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[3]/div[1]/button')
    improtParamentButton = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[3]/div[2]/div/button')
    importToast = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-message > div > div.el-dialog__body > div > div > p')
    addParamentFileButton = (By.ID, "expFile")
    addFileToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')
    sysUpgradeButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[4]/div/div/button')
    uploadFileToast = (By.XPATH,'/html/body/div[2]/div/div[2]/div/div/p')
    # sysUpgradeToast = (By.CSS_SELECTOR,'body > div.el-dialog__wrapper.xg-message.promo > div > div.el-dialog__body > div > div > p')
    uploadScheduleToast = (By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div/p')
    upgradeToRestartToast = (By.XPATH,'/html/body/div[2]/div/div[2]/div/div/p')

    addUpgradeFileButton = (By.XPATH, '//*[@id="proFile"]')


    def click_restartButton(self):
        restartButton = self.driver.find_element(*SysMaintenancePage.restartButton)
        self.driver.execute_script("arguments[0].click();", restartButton)

    def click_restartconfirmButton(self):
        restartconfirmButton = self.driver.find_element(*SysMaintenancePage.restartconfirmButton)
        self.driver.execute_script("arguments[0].click();", restartconfirmButton)

    def get_restartToast(self):
        text = self.driver.find_element(*SysMaintenancePage.restartToast).text
        return text

    def click_reFactorySetButton(self):
        reFactorySetButton = self.driver.find_element(*SysMaintenancePage.reFactorySetButton)
        self.driver.execute_script("arguments[0].click();", reFactorySetButton)

    def click_exportParamentButton(self):
        exportParamentButton = self.driver.find_element(*SysMaintenancePage.exportParamentButton)
        self.driver.execute_script("arguments[0].click();", exportParamentButton)

    def click_improtParamentButton(self):
        improtParamentButton = self.driver.find_element(*SysMaintenancePage.improtParamentButton)
        self.driver.execute_script("arguments[0].click();", improtParamentButton)

    def get_importToast(self):
        text = self.driver.find_element(*SysMaintenancePage.importToast).text
        return text

    def click_addParamentFileButton(self,fname):
        self.driver.find_element(*SysMaintenancePage.addParamentFileButton).send_keys(fname)

    def get_addFileToast(self):
        text = self.driver.find_element(*SysMaintenancePage.addFileToast).text
        return text

    def set_addParamentFileButton(self,fname):
        addParamentFileButton = self.driver.find_element(*SysMaintenancePage.addParamentFileButton)
        addParamentFileButton.send_keys(fname)

    def click_sysUpgradeButton(self):
        sysUpgradeButton = self.driver.find_element(*SysMaintenancePage.sysUpgradeButton)
        self.driver.execute_script("arguments[0].click();", sysUpgradeButton)

    # def get_sysUpgradeToast(self):
    #     text = self.driver.find_element(*SysMaintenancePage.sysUpgradeToast).text
    #     return text

    def click_addUpgradeFileButton(self,fname):
        addUpgradeFileButton = self.driver.find_element(*SysMaintenancePage.addUpgradeFileButton)
        addUpgradeFileButton.send_keys(fname)

    def get_uploadFileToast(self):
        text = self.driver.find_element(*SysMaintenancePage.uploadFileToast).text
        return text

    def get_uploadScheduleToast(self):
        text = self.driver.find_element(*SysMaintenancePage.uploadScheduleToast).text
        return text

    def get_upgradeToRestartToast(self):
        text = self.driver.find_element(*SysMaintenancePage.upgradeToRestartToast).text
        return text


