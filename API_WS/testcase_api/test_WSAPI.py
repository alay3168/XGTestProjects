#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2019-8-28
# @Description: FEIDAN_API
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

# dir = "testdata"
# case_yml = os.path.abspath(os.path.dirname(os.getcwd())) + "\\" + dir
case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../testdata"))

@ddt
class Web_Socket_Case(unittest.TestCase):

    # def get_socket(self):
    # # def __init__(self,*args,**kwargs):
    # #     # global WS
    # #     unittest.TestCase.__init__(self, *args, **kwargs)
    #     url = 'ws://10.58.122.205:8000'
    #
    #     data = {"Method": "Login",
    #             "Page": "Login",
    #             "Message": {"Login-Properties": {"UserName": "admin", "Passwd": "154vDmYO2qCYwP5+gusOiA=="}}}
    #     self.ws = websocket.create_connection(url)
    #     self.ws.send(json.dumps(data))

    @classmethod
    def setUpClass(cls):

        url = 'ws://10.58.122.205:8000'
        data = {"Method": "Login",
                "Page": "Login",
                "Message": {"Login-Properties": {"UserName": "admin", "Passwd": "154vDmYO2qCYwP5+gusOiA=="}}}
        cls.ws = websocket.create_connection(url)
        cls.ws.send(json.dumps(data))
        # return socket
        result = cls.ws.recv()
        print("Received '%s'" % result)

    @classmethod
    def tearDownClass(cls):
        cls.ws.close()
        print("------------执行用例结束-----------")


    @file_data(case_yml + "/GetConfig.yaml")
    def test_GetConfig_case(self, **test_data):
        # base_url = test_data.get('url')
        data = test_data.get('data')
        detail = test_data.get('detail')
        check = test_data.get('check')
        print detail
        self.ws.send(json.dumps(data))
        result = self.ws.recv()
        print("Received '%s'" % result)
        rec = json.loads(result)

        for c in check:
            for k,v in c.items():
                self.assertEqual(rec.get(k),v)

    @file_data(case_yml + "/SetConfig.yaml")
    def test_SetConfig_case(self, **test_data):
        # base_url = test_data.get('url')
        data = test_data.get('data')
        detail = test_data.get('detail')
        check = test_data.get('check')
        print detail
        # ws = websocket.create_connection(base_url)

        self.ws.send(json.dumps(data))
        result = self.ws.recv()
        print("Received '%s'" % result)
        rec = json.loads(result)

        for c in check:
            for k,v in c.items():
                self.assertEqual(rec.get(k),v)

if __name__ == '__main__':


    unittest.main()
    # 构造测试集
    # suite = unittest.TestSuite()
    # # 执行测试
    # runner = unittest.TextTestRunner()

    # runner.run(suite)
    # number = 1
    # while number<= 100:
    #     number+=1
    #     while True:
    #         try:
    #             unittest.main()
    #         except:
    #             print('exception')
    #         else:
    #             print('no exception')
