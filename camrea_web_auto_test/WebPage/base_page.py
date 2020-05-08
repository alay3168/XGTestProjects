#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import multiprocessing


class BasePage(object):
    # webdriver instance
    def __init__(self, driver):
        self.driver = driver

    def find(self, locator):
        '''查找元素，loctor = ("id", "kw")'''
        element = WebDriverWait(self.driver, 30, 0.5).until(EC.presence_of_element_located(locator))
        return element

    def click(self, locator):
        # '''点击元素'''
        # self.find(locator).click()
        self.driver.execute_script("arguments[0].click();", self.find(locator))

    def double_click(self, locator):
        '''双击事件'''
        element = self.find(locator)
        ActionChains(self.driver).double_click(element).perform()

    def set(self, locator, text):
        '''输入文本'''
        self.find(locator).send_keys(text)

    # def clear_content(self,locator):
    #     eml = self.driver.find_element(locator)
    #     eml.send_keys(Keys.CONTROL + 'a')
    #     eml.send_keys(Keys.DELETE)
    #
    def wait_eml_presence(self, locator):
        WebDriverWait(self.driver, 60, 0.3).until(EC.presence_of_element_located(locator))


class Login_page(BasePage):
    usename = (By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/input')
    password = (By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/input')
    login = (By.XPATH, '//*[@id="app"]/div/div[2]/div[4]/button')


class Home_image(BasePage):
    previewmenu = (By.CLASS_NAME, 'r_view')
    main_menu = (By.CLASS_NAME, 'menu')
    logout_menu = (By.CLASS_NAME, 'secede')
    image_default = (By.CLASS_NAME, 'recoverBtn')
    image_save = (By.CLASS_NAME, 'saveBtn')
    image_osd = (By.LINK_TEXT, "OSD设置")
    osd_default = (By.CLASS_NAME, 'recoverBtn')
    osd_save = (By.CLASS_NAME, 'saveBtn')

class Home_video(BasePage):
    video_encode = (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[2]/div/div[1]')
    encode_default = (By.CLASS_NAME, 'recoverBtn')
    encode_save = (By.CLASS_NAME, 'saveBtn')

class Home_audio(BasePage):
    audio_param = (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[3]/div/div[1]')
    param_save = (By.CLASS_NAME, 'saveBtn')

class Home_net(BasePage):
    net_tcp = (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[4]/div/div[1]')
    tcp_test = (By.CLASS_NAME, 'testBtn')
    tcp_save = (By.CLASS_NAME, 'saveBtn')
    net_ddns = (By.LINK_TEXT, 'DDNS')
    ddns_save = (By.CLASS_NAME, 'saveBtn')
    net_port = (By.LINK_TEXT, "端口和端口映射")
    port_upnp = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/button[2] ')
    upnp_save = (By.CLASS_NAME, 'saveBtn')
    net_GB = (By.LINK_TEXT, 'GB28181协议')
    GB_save = (By.CLASS_NAME, 'saveBtn')

class Home_intel(BasePage):
    intel_area = (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[5]/div/div[1]')
    area_save = (By.CLASS_NAME, 'saveBtn')
    intel_check = (By.LINK_TEXT, '检测类型')
    check_face = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[1]/div[1]/label')
    check_body = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div[1]/label')
    check_save = (By.CLASS_NAME, 'saveBtn')
    intel_protocol = (By.LINK_TEXT, '传输协议')
    protocol_test = (By.CLASS_NAME, 'testBtn')
    protocol_save = (By.CLASS_NAME, 'saveBtn')

class Home_alarm(BasePage):
    alarm_person= (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[6]/div/div[1]')
    person_detect = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[1]/label')
    person_save = (By.CLASS_NAME, 'saveBtn')
    alarm_shelter = (By.LINK_TEXT, '视频遮挡报警')
    shelter_switch = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[1]/label')
    shelter_save = (By.CLASS_NAME, 'saveBtn')
    alarm_unusual = (By.LINK_TEXT, '异常报警')
    unusual_off = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[1]/div[2]/label')
    unusual_offon = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div[2]/label')
    unusual_clash = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[1]/div[3]/label')
    unusual_clashon = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div[3]/label')
    unusual_call = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[1]/div[4]/label')
    unusual_callon = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div[4]/label[1]')
    unusual_callftp = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div[4]/label[2]')
    unusual_save = (By.CLASS_NAME, 'saveBtn')
    alarm_RS = (By.LINK_TEXT, 'RS485设置')
    RS_save = (By.CLASS_NAME, 'saveBtn')

class Home_sys(BasePage):
    sys_device = (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[7]/div/div[1]')
    sys_time = (By.LINK_TEXT, '时间设置')
    time_sny = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[3]/div[2]/div[2]')
    time_ntp = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[4]/label')
    time_manual = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/label')
    time_save = (By.CLASS_NAME, 'saveBtn')
    sys_safe = (By.LINK_TEXT, '安全设置')
    safe_save = (By.CLASS_NAME, 'saveBtn')

class Home_user(BasePage):
    user_setting = (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[8]/div/div[1]')
    user_add = (By.CLASS_NAME, 'operateBtn')
    add_rm = (By.CLASS_NAME, 'recoverBtn')

class Home_local(BasePage):
    local_service = (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[9]/div/div[1]')
    local_log = (By.LINK_TEXT, '日志')
    local_memory = (By.LINK_TEXT, '本地存储设置')

def run(url):
    while True:
        driver = webdriver.Chrome()
        driver.maximize_window()  # 最大化浏览器窗口
        LoginPage = Login_page(driver)
        LoginPage.driver.get(url)
        LoginPage.driver.implicitly_wait(30)

        #登录
        LoginPage.set(Login_page.usename, 'admin')
        LoginPage.set(Login_page.password, '123456')
        LoginPage.click(LoginPage.login)

        #图像设置
        homePage = Home_image(driver)
        homePage.click(Home_image.main_menu)
        sleep(3)
        homePage.click(homePage.image_default)
        sleep(3)
        homePage.click(homePage.image_save)
        sleep(3)
        homePage.click(homePage.image_osd)
        sleep(3)
        homePage.click(homePage.osd_default)
        sleep(3)
        homePage.click(homePage.osd_save)
        print("保存成功")
        sleep(3)

        # #视频设置
        homeVideo = Home_video(driver)
        homeVideo.click(homeVideo.video_encode)
        sleep(3)
        homeVideo.click(homeVideo.encode_default)
        sleep(3)
        homeVideo.click(homeVideo.encode_save)
        sleep(3)

        # #音频设置
        homeAudio = Home_audio(driver)
        homeAudio.click(homeAudio.audio_param)
        sleep(3)
        homeAudio.click(homeAudio.param_save)
        sleep(3)

        # #网络设置
        homenet = Home_net(driver)
        homenet.click(homenet.net_tcp)
        sleep(3)
        homenet.click(homenet.tcp_test)
        sleep(3)
        homenet.click(homenet.tcp_save)
        sleep(3)
        homenet.click(homenet.net_ddns)
        sleep(3)
        homenet.click(homenet.ddns_save)
        sleep(3)
        homenet.click(homenet.net_port)
        sleep(3)
        homenet.click(homenet.port_upnp)
        sleep(3)
        homenet.click(homenet.upnp_save)
        sleep(3)
        homenet.click(homenet.net_GB)
        sleep(3)
        homenet.click(homenet.GB_save)

        #智能分析
        homeintel = Home_intel(driver)
        homeintel.click(homeintel.intel_area)
        sleep(3)
        homeintel.click(homeintel.area_save)
        sleep(3)
        homeintel.click(homeintel.intel_check)
        sleep(3)
        homeintel.click(homeintel.check_face)
        sleep(2)
        homeintel.click(homeintel.check_body)
        sleep(2)
        homeintel.click(homeintel.check_save)
        sleep(3)
        homeintel.click(homeintel.intel_protocol)
        sleep(2)
        homeintel.click(homeintel.protocol_test)
        sleep(2)
        homeintel.click(homeintel.protocol_save)
        sleep(3)

        # #报警设置
        homeAlarm = Home_alarm(driver)
        homeAlarm.click(homeAlarm.alarm_person)
        homeAlarm.click(homeAlarm.person_detect)
        sleep(2)
        homeAlarm.click(homeAlarm.person_save)
        sleep(2)
        homeAlarm.click(homeAlarm.alarm_shelter)
        sleep(3)
        homeAlarm.click(homeAlarm.shelter_switch)
        sleep(2)
        homeAlarm.click(homeAlarm.shelter_save)
        sleep(3)
        homeAlarm.click(homeAlarm.alarm_unusual)
        homeAlarm.click(homeAlarm.unusual_off)
        homeAlarm.click(homeAlarm.unusual_offon)
        sleep(2)
        homeAlarm.click(homeAlarm.unusual_clash)
        homeAlarm.click(homeAlarm.unusual_clashon)
        sleep(2)
        homeAlarm.click(homeAlarm.unusual_call)
        homeAlarm.click(homeAlarm.unusual_callon)
        homeAlarm.click(homeAlarm.unusual_callftp)
        sleep(2)
        homeAlarm.click(homeAlarm.unusual_save)
        sleep(3)
        homeAlarm.click(homeAlarm.alarm_RS)
        homeAlarm.click(homeAlarm.RS_save)
        sleep(3)

        # #系统管理
        homesys = Home_sys(driver)
        homesys.click(homesys.sys_device)
        sleep(2)
        homesys.click(homesys.sys_time)
        homesys.click(homesys.time_sny)
        sleep(2)
        homesys.click(homesys.time_ntp)
        sleep(2)
        homesys.click(homesys.time_manual)
        homesys.click(homesys.time_save)
        sleep(3)
        homesys.click(homesys.sys_safe)
        homesys.click(homesys.safe_save)
        sleep(3)

        #用户管理
        homeUser = Home_user(driver)
        homeUser.click(homeUser.user_setting)
        sleep(2)
        homeUser.click(homeUser.user_add)
        sleep(3)
        homeUser.click(homeUser.add_rm)
        sleep(2)

        #本地设置
        homeLocal = Home_local(driver)
        homeLocal.click(homeLocal.local_service)
        sleep(2)
        homeLocal.click(homeLocal.local_log)
        sleep(2)
        homeLocal.click(homeLocal.local_memory)
        sleep(3)

        #跳至预览&退出关闭
        # homePage = Home_image(driver)
        homePage.click(Home_image.previewmenu)    #跳转至预览页面
        sleep(3)
        homePage.click(Home_image.logout_menu)  #退出摄像机管理后台
        sleep(3)
        driver.quit()

if __name__ == '__main__':
    urlList = ['http://10.58.122.115/','http://10.58.122.115/']

    for url in urlList:
        p = multiprocessing.Process(target=run, args=(url,))
        p.start()
        p1 = multiprocessing.Process(target=run, args=(url,))
        p1.start()
