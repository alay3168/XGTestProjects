#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/18 19:01   xushaohua      1.0         None
'''
import unittest
import os
from TestCase.test_login_page import *
from TestCase.test_home_page import *
from BeautifulReport import BeautifulReport as bf
import HtmlTestRunner
import HTMLTestRunner
import smtplib                         # 发送邮件模块
from email.mime.text import MIMEText   # 定义邮件内容
from email.header import Header        # 定义邮件标题
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_mail(latest_report):

    smtpserver = 'smtp.exmail.qq.com'
    # 发送邮箱用户名密码
    user = 'xushaohua@puppyrobot.com'
    password = 'mLkJa6vvj993YC5G'
    # 发送和接收邮箱
    sender = 'xushaohua@puppyrobot.com'
    receivers = ['alay929@163.com']

    # 发送邮件主题和内容
    subject = "Box Web 自动化测试报告"

    m = MIMEMultipart()
    m['Subject'] = subject
    m['From'] = sender
    m['To'] = ','.join(receivers)

    with open(latest_report,'rb') as file_obj:
        contents = file_obj.read()
    body = MIMEText(contents, _subtype='html',_charset='utf-8')
    m.attach(body)

    htmApart = MIMEApplication(open(latest_report, 'rb').read())
    htmApart.add_header('Content-Disposition', 'attachment', filename=latest_report)
    m.attach(htmApart)

    smtp = smtplib.SMTP(smtpserver, 25)
    smtp.login(user, password)

    print("Send email start...")
    smtp.sendmail(sender, receivers, m.as_string())
    smtp.quit()
    print("Email send end!")


def latest_report(report_dir):
    lists = os.listdir(report_dir)
    print(lists)
    # 按时间顺序对该目录文件夹下面的文件进行排序
    lists.sort(key=lambda fn: os.path.getatime(report_dir + "\\" + fn))
    print("The latest report is:" + lists[-1])

    file = os.path.join(report_dir, lists[-1])
    print(file)
    return file

if __name__ == '__main__':

    suite = unittest.TestSuite()  # 测试套件
    loader = unittest.TestLoader()  # 用例加载器
    test_loginclass = loader.loadTestsFromTestCase(TestLoginPage)  # 加载测试类
    test_homepageclass = loader.loadTestsFromTestCase(TestHomePage)
    suite.addTest(test_loginclass)  # 测试类添加到测试套件中
    suite.addTest(test_homepageclass)
    run = bf(suite)  # 实例化BeautifulReport模块

    localtime = time.asctime(time.localtime(time.time()))
    time=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    testReportFileName = time +'-TestReport'
    run.report(filename=testReportFileName, description='抓拍盒UI自动化测试')

    reportDir = os.getcwd()
    report = latest_report(reportDir)
    send_mail(report)

    # for i in range(1,10000):
    #     TestLoginPage_suit()
    #     print("运行次数：",i)

        