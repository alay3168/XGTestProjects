from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from BoxWebAutoTest.pageManager.BasePage import BasePage
import time


class LoginPage(BasePage):
    """description of class"""
    # page element identifier
    usename = (By.NAME, 'username')
    password = (By.NAME, 'password')
    # dialogTitle = (By.XPATH, "//h3[@class=\"modal-title ng-binding\"]")
    # cancelButton = (By.XPATH, '//button[@class=\"btn btn-warning ng-binding\"][@ng-click=\"cancel()\"]')
    okButton = (By.CSS_SELECTOR, ".el-button")

    # Get username textbox and input username
    def set_username(self, username):
        name = self.driver.find_element(*LoginPage.usename)
        name.send_keys(username)

        # Get password textbox and input password, then hit return

    def set_password(self, password):
        pwd = self.driver.find_element(*LoginPage.password)
        pwd.send_keys(password + Keys.RETURN)

        # Get pop up dialog title

    # def get_DiaglogTitle(self):
    #     digTitle = self.driver.find_element(*LoginPage.dialogTitle)
    #     return digTitle.text

        # Get "cancel" button and then click

    # def click_cancel(self):
    #     cancelbtn = self.driver.find_element(*LoginPage.cancelButton)
    #     cancelbtn.click()

        # click Sign in

    def click_SignIn(self):
        # driver.refresh
        okbtn = self.driver.find_element(*LoginPage.okButton)
        okbtn.click()


    # def run(self):
    #     driver = webdriver.Chrome()
    #
    #     driver.get("http://10.58.122.201/")
    #     driver.implicitly_wait(30)
    #
    #     self.set_username("admin")
    #     self.set_password("123456")
    #     self.click_SignIn()
    #     time.sleep(3)
    #     driver.close()

if __name__ == "__main__":

    driver = webdriver.Chrome()
    LoginPage = LoginPage(driver)

    LoginPage.driver.get("http://10.58.122.201/")
    LoginPage.driver.implicitly_wait(30)

    LoginPage.set_username("admin")
    LoginPage.set_password("123456")
    LoginPage.click_SignIn()
    time.sleep(3)
    LoginPage.driver.close()