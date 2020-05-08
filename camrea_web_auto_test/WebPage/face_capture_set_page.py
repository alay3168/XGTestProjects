#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   face_capture_set_page.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 17:09   xushaohua      1.0         None
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from WebPage.base_page import BasePage


class FaceCaptureSetPage(BasePage):
    # page element identifier
    faceCaptureButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/label[1]/span')
    picturePushIntervaLower = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[1]/div/div/span[1]')
    picturePushIntervaNum = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[1]/div/div/div/input')
    picturePushIntervaUp = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[1]/div/div/span[2]')
    picturePushIntervaErrToast = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[1]/div/div[2]')

    picturePushNumberLower = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[2]/div/div/span[1]')
    picturePushNumberNum = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[2]/div/div/div/input')
    picturePushNumberUp = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[2]/div/div/span[2]')
    picturePushNumberErrToast = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[2]/div/div[2]')

    horizontalAngleLower = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[3]/div/div/span[1]')
    horizontalAngleNum = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[3]/div/div/div/input')
    horizontalAngleUp = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[3]/div/div/span[2]')
    horizontalAngleErrToast = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[3]/div/div[2]')

    pitchingAngleLower = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[4]/div/div/span[1]')
    pitchingAngleNum = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[4]/div/div/div/input')
    pitchingAngleUp = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[4]/div/div/span[2]')
    pitchingAngleErrToast = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[4]/div/div[2]')

    horizontalTiltAngleLower = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[5]/div/div/span[1]')
    horizontalTiltAngleNum = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[5]/div/div/div/input')
    horizontalTiltAngleUp = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[5]/div/div/span[2]')
    horizontalTiltAngleErrToast = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[5]/div/div[2]')

    miniCaptureFaceOptions = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[6]/div/div/div/input')
    miniCaptureFaceOptions30 = (By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[1]')
    miniCaptureFaceOptions60 = (By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[2]')
    miniCaptureFaceOptions100 = (By.XPATH, '/html/body/div[2]/div[1]/div[1]/ul/li[3]')

    saveButton = (By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/section/div/div[2]/form/div[7]/div/button/span')
    saveSuccessToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')

    def click_faceCaptureButton(self):
        fcb = self.driver.find_element(*FaceCaptureSetPage.faceCaptureButton)
        self.driver.execute_script("arguments[0].click();", fcb)

    def click_picturePushIntervaLower(self):
        picturePushIntervaLower = self.driver.find_element(*FaceCaptureSetPage.picturePushIntervaLower)
        # self.driver.execute_script("arguments[0].click();", picturePushIntervaLower)
        picturePushIntervaLower.click()
    def clear_picturePushIntervaNum(self):
        eml = self.driver.find_element(*FaceCaptureSetPage.picturePushIntervaNum)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)
    def set_picturePushIntervaNum(self,num):
        eml = self.driver.find_element(*FaceCaptureSetPage.picturePushIntervaNum)
        eml.send_keys(num)
    def click_picturePushIntervaUp(self):
        picturePushIntervaUp = self.driver.find_element(*FaceCaptureSetPage.picturePushIntervaUp)
        # self.driver.execute_script("arguments[0].click();", picturePushIntervaUp)
        picturePushIntervaUp.click()
    def get_picturePushIntervaErrToast(self):
        text = self.driver.find_element(*FaceCaptureSetPage.picturePushIntervaErrToast).text
        return text

    def click_picturePushNumberLower(self):
        picturePushNumberLower = self.driver.find_element(*FaceCaptureSetPage.picturePushNumberLower)
        # self.driver.execute_script("arguments[0].click();", picturePushNumberLower)
        picturePushNumberLower.click()
    def clear_picturePushNumberNum(self):
        eml = self.driver.find_element(*FaceCaptureSetPage.picturePushNumberNum)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)
    def set_picturePushNumberNum(self,num):
        eml = self.driver.find_element(*FaceCaptureSetPage.picturePushNumberNum)
        eml.send_keys(num)
    def click_picturePushNumberUp(self):
        picturePushNumberUp = self.driver.find_element(*FaceCaptureSetPage.picturePushNumberUp)
        # self.driver.execute_script("arguments[0].click();", picturePushNumberUp)
        picturePushNumberUp.click()
    def get_picturePushNumberErrToast(self):
        text = self.driver.find_element(*FaceCaptureSetPage.picturePushNumberErrToast).text
        return text

    def click_horizontalAngleLower(self):
        horizontalAngleLower = self.driver.find_element(*FaceCaptureSetPage.horizontalAngleLower)
        # self.driver.execute_script("arguments[0].click();", horizontalAngleLower)
        horizontalAngleLower.click()
    def clear_horizontalAngleNum(self):
        eml = self.driver.find_element(*FaceCaptureSetPage.horizontalAngleNum)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)
    def set_horizontalAngleNum(self,num):
        eml = self.driver.find_element(*FaceCaptureSetPage.horizontalAngleNum)
        eml.send_keys(num)
    def click_horizontalAngleUp(self):
        horizontalAngleUp = self.driver.find_element(*FaceCaptureSetPage.horizontalAngleUp)
        # self.driver.execute_script("arguments[0].click();", horizontalAngleUp)
        horizontalAngleUp.click()
    def get_horizontalAngleErrToast(self):
        text = self.driver.find_element(*FaceCaptureSetPage.horizontalAngleErrToast).text
        return text

    def click_horizontalTiltAngleLower(self):
        horizontalTiltAngleLower = self.driver.find_element(*FaceCaptureSetPage.horizontalTiltAngleLower)
        # self.driver.execute_script("arguments[0].click();", horizontalTiltAngleLower)
        horizontalTiltAngleLower.click()
    def clear_horizontalTiltAngleNum(self):
        eml = self.driver.find_element(*FaceCaptureSetPage.horizontalTiltAngleNum)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)
    def set_horizontalTiltAngleNum(self,num):
        eml = self.driver.find_element(*FaceCaptureSetPage.horizontalTiltAngleNum)
        eml.send_keys(num)
    def click_horizontalTiltAngleUp(self):
        horizontalTiltAngleUp = self.driver.find_element(*FaceCaptureSetPage.horizontalTiltAngleUp)
        # self.driver.execute_script("arguments[0].click();", pitchingAngleLower)
        horizontalTiltAngleUp.click()
    def get_horizontalTiltAngleErrToast(self):
        text = self.driver.find_element(*FaceCaptureSetPage.horizontalTiltAngleErrToast).text
        return text

    def click_pitchingAngleLower(self):
        pitchingAngleLower = self.driver.find_element(*FaceCaptureSetPage.pitchingAngleLower)
        # self.driver.execute_script("arguments[0].click();", pitchingAngleUp)
        pitchingAngleLower.click()
    def clear_pitchingAngleNum(self):
        eml = self.driver.find_element(*FaceCaptureSetPage.pitchingAngleNum)
        eml.send_keys(Keys.CONTROL + 'a')
        eml.send_keys(Keys.DELETE)
    def set_pitchingAngleNum(self,num):
        eml = self.driver.find_element(*FaceCaptureSetPage.pitchingAngleNum)
        eml.send_keys(num)
    def click_pitchingAngleUp(self):
        pitchingAngleUp = self.driver.find_element(*FaceCaptureSetPage.pitchingAngleUp)
        # self.driver.execute_script("arguments[0].click();", pitchingAngleUp)
        pitchingAngleUp.click()
    def get_pitchingAngleErrToast(self):
        text = self.driver.find_element(*FaceCaptureSetPage.pitchingAngleErrToast).text
        return text

    def click_miniCaptureFaceOptions(self):
        miniCaptureFaceOptions = self.driver.find_element(*FaceCaptureSetPage.miniCaptureFaceOptions)
        # self.driver.execute_script("arguments[0].click();", miniCaptureFaceOptions)
        miniCaptureFaceOptions.click()
    def select_miniCaptureFaceOptions30(self):
        miniCaptureFaceOptions30 = self.driver.find_element(*FaceCaptureSetPage.miniCaptureFaceOptions30)
        self.driver.execute_script("arguments[0].click();", miniCaptureFaceOptions30)
    def select_miniCaptureFaceOptions60(self):
        miniCaptureFaceOptions60 = self.driver.find_element(*FaceCaptureSetPage.miniCaptureFaceOptions60)
        self.driver.execute_script("arguments[0].click();", miniCaptureFaceOptions60)
    def select_miniCaptureFaceOptions100(self):
        miniCaptureFaceOptions100 = self.driver.find_element(*FaceCaptureSetPage.miniCaptureFaceOptions100)
        self.driver.execute_script("arguments[0].click();", miniCaptureFaceOptions100)

    def click_saveButton(self):
        csb = self.driver.find_element(*FaceCaptureSetPage.saveButton)
        self.driver.execute_script("arguments[0].click();", csb)
    def get_saveSuccessToast(self):
        text = self.driver.find_element(*FaceCaptureSetPage.saveSuccessToast).text
        return text