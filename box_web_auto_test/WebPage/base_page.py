#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   33.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/18 12:51   xushaohua      1.0         None
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time

class BasePage(object):
    # webdriver instance
    def __init__(self, driver):
        self.driver = driver

    def find(self, locator):
        '''查找元素，loctor = ("id", "kw")'''
        element = WebDriverWait(self.driver, 30, 0.5).until(EC.presence_of_element_located(locator))
        return element

    def click(self, locator):
        '''点击元素'''
        self.find(locator).click()

    def double_click(self, locator):
        '''双击事件'''
        element = self.find(locator)
        ActionChains(self.driver).double_click(element).perform()

    def send(self, locator, text):
        '''输入文本'''
        self.find(locator).send_keys(text)

    # def clear_content(self,locator):
    #     eml = self.driver.find_element(locator)
    #     eml.send_keys(Keys.CONTROL + 'a')
    #     eml.send_keys(Keys.DELETE)
    #
    def wait_eml_presence(self,locator):
        WebDriverWait(self.driver, 60, 0.3).until(EC.presence_of_element_located(locator))