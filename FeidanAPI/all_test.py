#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2019-8-28
# @Description: FEIDAN_API
#****************************************************************
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
        pattern ='*.py',top_level_dir=None)

    #discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)
            print testunit
    return testunit


alltestnames = creatsuite1()

now = time.strftime("%Y-%m-%d %H-%M-%S")
#定义个报告存放路径，支持相对路径。
filename = os.getcwd() + "/report/" +now+'RESULT.html'

fp = file(filename, 'wb')
runner =HTMLTestRunner.HTMLTestRunner(
    stream=fp,
    title=u'防飞单-接口自动化测试报告',
    description=u'用例执行情况：')

#执行测试用例

# ========查找最新测试报告，调用发邮件功能=====
def sendreport():
    result_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"report")
    print result_dir
    lists = os.listdir(result_dir)
    lists.sort(
        key=lambda fn: os.path.getmtime(result_dir + "\\" + fn) if not os.path.isdir(result_dir + "\\" + fn) else 0)
    # 找到最新生成的文件
    file_new = os.path.join(result_dir, lists[-1])
    print file_new

    # 调用发邮件模块
    sentmail(file_new)

# =======定义发送邮件========
def sentmail(file_new):
    # 发信邮箱
    mail_from = 'autotest@puppyrobot.com'
    # 收信邮箱
    mail_to = 'suzhao@puppyrobot.com'
    # 定义正文
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    msg = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    # 定义标题
    msg['Subject'] = u"防飞单系统接口自动化测试报告"
    # 定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp = smtplib.SMTP()
    # 连接SMTP服务器
    smtp.connect('smtp.exmail.qq.com')
    # 用户名密码
    smtp.login('autotest@puppyrobot.com', '1qaz2wsx!QAZ')
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.quit()
    print 'email has send out !'

# runner.run(alltestnames)
if __name__ == '__main__':
    runner.run(alltestnames)
    fp.close()
    sendreport()
