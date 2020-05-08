#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : xushaohua
# @Version    : 1.0
# @Date       : 2019-8-28
# @Description: FEIDAN_API
#****************************************************************



# import os
# import time
# i = 0
# while True:
#   i = i + 1
#   dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "./testcase_api/test_WSAPI.py"))
#   # os.system("sudo ./batch_uploader ./dump")
#   os.system("python" +dir)
#   print"+++++++++++++++++++++++++++++++"
#   print"times:" ,i
#   time.sleep(15)

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import unittest
import HTMLTestRunner
import HTMLTestRunnerEN
import os ,time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib

dir = "testcase_api"
# case_dir = os.getcwd() + "\\" + dir
case_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),dir)
print case_dir

def creatsuite1():
    testunit=unittest.TestSuite()
    #discover 方法定义
    discover=unittest.defaultTestLoader.discover(case_dir,
        pattern ='test_WSAPI.py',top_level_dir=None)

    # discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)
            print testunit
    return testunit

now = time.strftime("%Y-%m-%d %H-%M-%S")
#定义个报告存放路径，支持相对路径。
filename = os.getcwd() + "/report/" +now+'RESULT.html'


alltestnames = creatsuite1()

# fp = file(filename, 'wb')
# runner =HTMLTestRunner.HTMLTestRunner(
#     stream=fp,
#     title=u'抓拍盒-接口自动化测试报告',
#     description=u'用例执行情况：')




if __name__ == '__main__':
    i = 0
    while True:
        creatsuite1()
        # runner.run(alltestnames)
        # fp.close()
        i = i + 1
        print"+++++++++++++++++++++++++++++++"
        print"times:" ,i
        time.sleep(15)
    fp.close()







