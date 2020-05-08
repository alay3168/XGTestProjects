#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : xushaohua
# @Version    : 1.0
# @Date       : 2019-8-28
# @Description: FEIDAN_API
#****************************************************************
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import unittest
from BeautifulReport import BeautifulReport
import os ,time

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

current_path = os.getcwd()
report_path = os.path.join(current_path, "Report")
now = time.strftime("%Y-%m-%d %H-%M-%S")
#定义个报告存放路径，支持相对路径。
report_title = os.getcwd() + "/report/" +now+'RESULT.html'


alltestnames = creatsuite1()

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    run = BeautifulReport(testsuite)
    run.report(description=desc, filename=report_title, log_path=report_path)