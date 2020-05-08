#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2018-8-08
# @Description: 智能监控平台API
#****************************************************************

import unittest
import requests
import sys
sys.path.append("..")
from testdata import request_param
from conf import setup



class StaffTestCase(setup.MyTest):


    def test_staff_register1(self):
        u'''1.新增人员-新人员注册-正常注册'''

        r = requests.post(self.url('peoples'),data = request_param.register1(),headers = self.headers)
        self.code = r.status_code
        self.text = r.text
        result = r.json()
        self.assertEqual(self.code,200)
        self.assertEqual(result['data']['Name'],u'自动化testA')
        self.assertTrue('ClusterId'in self.text)

    def test_staff_register2(self):
        u'''2.新增人员-未填验证-未传入image1'''

        r = requests.post(self.url('peoples'),data = request_param.register2(),headers = self.headers)
        self.code = r.status_code
        self.text = r.text
        result = r.json()
        self.assertEqual(result['err_code'],30004)
        self.assertEqual(result['err_msg'],u'image 1 cannot be empty')

    def test_staff_register3(self):
        u'''3.新增人员-必填验证-未传入type'''

        r = requests.post(self.url('peoples'),data = request_param.register3(),headers = self.headers)
        self.code = r.status_code
        self.text = r.text
        result = r.json()
        self.assertEqual(result['err_code'],30003)
        self.assertEqual(result['err_msg'],u'people must be in staff or blacklist')

    def test_staff_register4(self):
        u'''4.新增人员-必填验证-未传入attribute'''

        r = requests.post(self.url('peoples'),data = request_param.register4(),headers = self.headers)
        self.code = r.status_code
        self.text = r.text
        result = r.json()
        # self.assertEqual(result['err_code'],30003)
        # self.assertEqual(result['err_msg'],u'people must be in staff or blacklist')

    # @classmethod
    # def staff_registe(self):
    #     r = requests.post(self.url('peoples'), data=request_param.register1(), headers=self.headers)
    #     result = r.json()
    #     data = result['id']
    #     return data
    #
    # def staff_query1(self):
    #
    #     r = requests.get(self.url('peoples'),params = data,headers = self.headers)








    def url(self, path):
        return self.domain + path



if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(StaffTestCase("test_staff_register1"))
    suite.addTest(StaffTestCase("test_staff_register2"))
    suite.addTest(StaffTestCase("test_staff_register3"))
    suite.addTest(StaffTestCase("test_staff_register4"))



    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    #unittest.main()

