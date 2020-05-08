#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest, time
import  xml.dom.minidom

#引入xml文件
dom = xml.dom.minidom.parse('E:\\selenium_test_case\\data\\info.xml')
root = dom.documentElement


#openurl
uu=dom.getElementsByTagName('openurl')
u=uu[0]
geturl=u.firstChild.data

def openurl(self):
    u = geturl
    return u


#登陆用户名密码
itemlist = root.getElementsByTagName('openlogin')
item = itemlist[0]
username=item.getAttribute("username")
passwd=item.getAttribute("passwd")


#登陆
def login(self):
    driver = self.driver
    we = self.we
    driver.maximize_window() #浏览器全屏
    we.findId(driver,"user_name").clear()
    we.findId(driver,"user_name").send_keys(username)
    we.findId(driver,"user_pwd").clear()
    we.findId(driver,"user_pwd").send_keys(passwd)
    we.findId(driver,"dl_an_submit").click()
    time.sleep(3)
    #we.findClassName(driver,"guide-ok-btn").click() #新功能引导
    #time.sleep(2)


#退出模块
def logout(self):
    driver = self.driver
    we = self.we
    we.findClassName(driver,"Usertool").click()
    time.sleep(2)
    we.findLinkText(driver,"退出").click()
    time.sleep(2)




   
