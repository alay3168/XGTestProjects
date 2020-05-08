#coding=utf-8
import unittest
import HTMLTestRunner
import os ,time


list='E:\\YOP_OPENAPI\\test_case'

def creatsuitel():
    testunit=unittest.TestSuite()
    #discover 方法定义
    discover=unittest.defaultTestLoader.discover(list,
    	pattern ='*_sta.py',top_level_dir=None)


    #discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)
            print testunit
    return testunit


alltestnames = creatsuitel()


now = time.strftime("%Y-%m-%d %H-%M-%S")
#定义个报告存放路径，支持相对路径。
filename = 'E:\\YOP_OPENAPI\\report\\'+now+'RESULT.html'

fp = file(filename, 'wb')
runner =HTMLTestRunner.HTMLTestRunner(
	stream=fp,
	title=u'YOP组线下回归自动化接口测试报告',
	description=u'用例执行情况：')

#执行测试用例
runner.run(alltestnames)

#==================
# unittest.suite.TestSuite
# tests=[
# <uuinterface_test.InterfaceTestCase testMethod=test_baidu_search>]