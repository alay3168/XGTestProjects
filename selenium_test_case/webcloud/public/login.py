#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest, time
import csv  #导入csv包
import  xml.dom.minidom

#引入xml文件
dom = xml.dom.minidom.parse('E:\\selenium_test_case\\data\\info.xml')
root = dom.documentElement


#浏览器
bb=dom.getElementsByTagName('browser')
b=bb[0]
br=b.firstChild.data


def browser(self):
    driver =webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                              desired_capabilities={'platform': 'ANY',
                                                    'browserName':br,
                                                    'version': '',
                                                    'javascriptEnabled': True,
                                                    })
    return driver


#url
uu=dom.getElementsByTagName('url')
u=uu[0]
geturl=u.firstChild.data

def url(self):
    u = geturl
    return u


#登陆用户名密码
itemlist = root.getElementsByTagName('login')
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
    we.findClassName(driver,"guide-ok-btn").click() #新功能引导
    time.sleep(2)


#退出模块
def logout(self):
    driver = self.driver
    we = self.we
    we.findClassName(driver,"Usertool").click()
    time.sleep(2)
    we.findLinkText(driver,"退出").click()
    time.sleep(2)


#webcloud url
uu=dom.getElementsByTagName('webcloud_url')
u=uu[0]
weburl=u.firstChild.data

def webcloud_url(self):
    u = weburl
    return u

   




