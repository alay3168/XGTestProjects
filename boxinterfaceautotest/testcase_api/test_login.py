#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : xushaohua
# @Version    : 1.0
# @Date       : 2020-2-28
# @Description: Ibox_API
#****************************************************************

import websocket
import unittest
import json
import sys
import yaml
sys.path.append("..")
# from common import conf
from ddt import ddt,file_data,unpack,data
import os,time

case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../testdata"))

@ddt
class APITestCase(unittest.TestCase):
    @file_data(case_yml + "/login.yaml")
    def test_Login_case(self, **test_data):
        u"""登录"""
        url = test_data.get('url')
        data = test_data.get('data')
        detail = test_data.get('detail')
        check = test_data.get('check')
        print(detail)
        self.ws = websocket.create_connection(url)
        self.ws.send(json.dumps(data))
        result = self.ws.recv()
        print("Received '%s'" % result)
        rec = json.loads(result)

        for c in check:
            for k,v in c.items():
                self.assertEqual(rec.get(k),v)

    # @file_data(case_yml + "/logout.yaml")
    # def test_Logout_case(self, **test_data):
    #     u"""登出"""
    #     url = test_data.get('url')
    #     data = test_data.get('data')
    #     detail = test_data.get('detail')
    #     check = test_data.get('check')
    #     print(detail)
    #     self.ws = websocket.create_connection(url)
    #     self.ws.send(json.dumps(data))
    #     result = self.ws.recv()
    #     print("Received '%s'" % result)
    #     rec = json.loads(result)
    #
    #     for c in check:
    #         for k,v in c.items():
    #             self.assertEqual(rec.get(k),v)


if __name__ == '__main__':
    # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(APITestCase("test_Login_case"))
    # suite.addTest(APITestCase("test_Logout_case"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    unittest.main()
