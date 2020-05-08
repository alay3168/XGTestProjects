from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from WebPage.base_page import BasePage
import time

class LoginPage(BasePage):
    """description of class"""
    # page element identifier
    usename = (By.NAME, 'username')
    password = (By.NAME, 'password')
    login = (By.CSS_SELECTOR,'#app > div > div > div.main_right > p')
    okButton = (By.CSS_SELECTOR, ".el-button")
    pwderrToast = (By.CSS_SELECTOR,'body > div.el-message.el-message--error > p')
    usenameNulltoast = (By.CSS_SELECTOR,'#app > div > div > div.main_right > form > div:nth-child(1) > div > div.el-form-item__error')
    pwdNulltoast = (By.CSS_SELECTOR, '#app > div > div > div.main_right > form > div:nth-child(2) > div > div.el-form-item__error')
    pwdOverlengthToast = (By.CSS_SELECTOR,'#app > div > div > div.main_right > form > div.el-form-item.input-item.is-error.is-required > div > div.el-form-item__error')

    # Get username textbox and input username
    def set_username(self, username):
        name = self.driver.find_element(*LoginPage.usename)
        name.send_keys(username)

    # Get password textbox and input password, then hit return
    def set_password(self, password):
        pwd = self.driver.find_element(*LoginPage.password)
        pwd.send_keys(password)

    def click_SignIn(self):
        # driver.refresh
        okbtn = self.driver.find_element(*LoginPage.okButton)
        # okbtn.click()
        self.driver.execute_script("arguments[0].click();", okbtn)

    def get_pwderrToast(self):
        # driver.refresh
         return self.driver.find_element(*LoginPage.pwderrToast).text

    def get_usenameNulltoast(self):
        # driver.refresh
         return self.driver.find_element(*LoginPage.usenameNulltoast).text

    def get_pwdNulltoast(self):
        # driver.refresh
         return self.driver.find_element(*LoginPage.pwdNulltoast).text

    def get_pwdOverlengthToast(self):
        # driver.refresh
         return self.driver.find_element(*LoginPage.pwdOverlengthToast).text

    def get_login(self):
        # driver.refresh
         return self.driver.find_element(*LoginPage.login).text

if __name__ == "__main__":

    driver = webdriver.Chrome()
    LoginPage = LoginPage(driver)

    LoginPage.driver.get("http://10.58.122.201/")
    LoginPage.driver.implicitly_wait(30)

    LoginPage.set_username("admin")
    LoginPage.set_password("1234567")
    LoginPage.click_SignIn()
    time.sleep(3)
    print('get_errToast',LoginPage.get_errToast())
    LoginPage.driver.close()