#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   user_manage_page.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/25 17:10   xushaohua      1.0         None
'''

from WebPage.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class UserManagePage(BasePage):

    addUserButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/div[3]/table/tbody/tr[1]/td[4]/div/button[1]')
    modifyUserButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/div[3]/table/tbody/tr[2]/td[4]/div/button[2]/span')
    deleteUserButton = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/div[3]/table/tbody/tr[2]/td[4]/div/button[3]/span')
    deleteConfirmButton = (By.XPATH,'/html/body/div[6]/div/div[3]/div/button[2]/span')
    deleteCancelmButton = (By.XPATH, '/html/body/div[6]/div/div[3]/div/button[1]/span')
    addUserSuccessToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--success > p')
    addUserFailToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--error > p')


    def click_addUserButton(self):
        addUserButton = self.driver.find_element(*UserManagePage.addUserButton)
        self.driver.execute_script("arguments[0].click();", addUserButton)

    def click_modifyUserButton(self):
        modifyUserButton = self.driver.find_element(*UserManagePage.modifyUserButton)
        self.driver.execute_script("arguments[0].click();", modifyUserButton)

    def click_deleteUserButton(self):
        deleteUserButton = self.driver.find_element(*UserManagePage.deleteUserButton)
        self.driver.execute_script("arguments[0].click();", deleteUserButton)

    def click_deleteConfirmButton(self):
        deleteConfirmButton = self.driver.find_element(*UserManagePage.deleteConfirmButton)
        self.driver.execute_script("arguments[0].click();", deleteConfirmButton)

    def get_addUserSuccessToast(self):
        return self.driver.find_element(*UserManagePage.addUserSuccessToast).text

    def get_addUserFailToast(self):
        return self.driver.find_element(*UserManagePage.addUserFailToast).text

    def delete_user_list(self):
        arr=[]
        videoList = []
        table_loc = (By.XPATH,'//*[@id="app"]/div/div/section/div/div[2]/section/div/div[1]/div[3]/table/tbody')
        table_tr_list = self.driver.find_element(*table_loc).find_elements(By.TAG_NAME,'tr')
        for tr in table_tr_list:
            print(tr)
        # if len(table_tr_list)>0:
        #     for tr in table_tr_list:
        #         arr1 = (tr.text).split(' ')
        #         # print(arr1)
        #         arr.append(arr1)
        #     for i in range(len(arr)):
        #         li = []
        #         for j in range(len(arr[i])):
        #             arr1 = arr[i][j].split('\n')
        #             li = li +arr1
        #         videoList.append(li)
        # return videoList

    class AddUserPage(BasePage):
        userNameField = (By.XPATH,'/html/body/div[2]/div/div[2]/div/div/form/div[1]/div/div/input')
        userTypeField =  (By.XPATH,'/html/body/div[2]/div/div[2]/div/div/form/div[2]/div/div/div[1]/input')
        operatorOption = (By.XPATH,'/html/body/div[4]/div[1]/div[1]/ul/li[1]/span')
        managerOption = (By.XPATH,'/html/body/div[4]/div[1]/div[1]/ul/li[2]/span')
        pwdField = (By.XPATH,'/html/body/div[2]/div/div[2]/div/div/form/div[3]/div/div/input')
        pwdConfirmField = (By.XPATH,'/html/body/div[2]/div/div[2]/div/div/form/div[4]/div/div/input')
        cancelButton = (By.XPATH,'/html/body/div[2]/div/div[3]/div/button[2]/span')
        saveButton = (By.XPATH, '/html/body/div[2]/div/div[3]/div/button[1]/span')

        def set_userNameField(self,userName):
            userNameField = self.driver.find_element(*self.userNameField)
            userNameField.send_keys(userName)

        def click_userTypeField(self):
            cutf = self.driver.find_element(*self.userTypeField)
            self.driver.execute_script("arguments[0].click();", cutf)

        def set_operatorOptionType(self):
            operatorOption = self.driver.find_element(*self.operatorOption)
            self.driver.execute_script("arguments[0].click();", operatorOption)

        def set_managerOptionType(self):
            managerOption = self.driver.find_element(*self.managerOption)
            self.driver.execute_script("arguments[0].click();", managerOption)

        def set_pwdField(self,pwd):
            pwdField = self.driver.find_element(*self.pwdField)
            pwdField.send_keys(pwd)

        def set_pwdConfirmField(self,pwd):
            pwdConfirmField = self.driver.find_element(*self.pwdConfirmField)
            pwdConfirmField.send_keys(pwd)

        def click_cancelButton(self):
            cutf = self.driver.find_element(*self.cancelButton)
            self.driver.execute_script("arguments[0].click();", cutf)

        def click_saveButton(self):
            cutf = self.driver.find_element(*self.saveButton)
            self.driver.execute_script("arguments[0].click();", cutf)

    class ModifyuserPage(BasePage):
        userNameField = (By.XPATH, '/html/body/div[2]/div/div[2]/div/div/form/div[1]/div/div/input')
        userTypeField = (By.XPATH, '/html/body/div[2]/div/div[2]/div/div/form/div[2]/div/div/div[1]/input')
        operatorOption = (By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[1]')
        managerOption = (By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[2]/span')
        cancelButton = (By.XPATH, '/html/body/div[2]/div/div[3]/div/button[2]/span')
        saveButton = (By.XPATH, '/html/body/div[2]/div/div[3]/div/button[1]/span')

        def clear_userName(self):
            eml = self.driver.find_element(*self.userNameField)
            eml.send_keys(Keys.CONTROL + 'a')
            eml.send_keys(Keys.DELETE)

        def set_userName(self,name):
            userNameField = self.driver.find_element(*self.userNameField)
            userNameField.send_keys(name)

        def click_userTypeField(self):
            cutf = self.driver.find_element(*self.userTypeField)
            self.driver.execute_script("arguments[0].click();", cutf)

        def set_operatorOptionType(self):
            operatorOption = self.driver.find_element(*self.operatorOption)
            self.driver.execute_script("arguments[0].click();", operatorOption)

        def set_managerOptionType(self):
            managerOption = self.driver.find_element(*self.managerOption)
            self.driver.execute_script("arguments[0].click();", managerOption)

        def click_cancelButton(self):
            cutf = self.driver.find_element(*self.cancelButton)
            self.driver.execute_script("arguments[0].click();", cutf)

        def click_saveButton(self):
            cutf = self.driver.find_element(*self.saveButton)
            self.driver.execute_script("arguments[0].click();", cutf)

if __name__ == '__main__':
    pass