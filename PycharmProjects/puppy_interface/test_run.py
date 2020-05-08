#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import HTMLTestRunner
import os ,time

dir = "testcase"
case_dir = os.getcwd() + "/" + dir
print case_dir


def creatsuitel():

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


alltestnames = creatsuitel()


now = time.strftime("%Y-%m-%d %H-%M-%S")
#定义个报告存放路径，支持相对路径。
filename = os.getcwd() + "/report/" +now+'RESULT.html'

fp = file(filename, 'wb')
runner =HTMLTestRunner.HTMLTestRunner(
	stream=fp,
	title=u'人脸识别监控平台-接口自动化测试报告',
	description=u'用例执行情况：')

#执行测试用例

runner.run(alltestnames)