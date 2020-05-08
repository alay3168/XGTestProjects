#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2019-8-28
# @Description: FEIDAN_API
#****************************************************************

import unittest
import requests
import json
import sys
import yaml
sys.path.append("..")
from common import conf
from ddt import ddt,file_data,unpack,data
import os

# dir = "testdata"
# case_yml = os.path.abspath(os.path.dirname(os.getcwd())) + "\\" + dir
case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../testdata"))

@ddt
class CardfaceTestCase(conf.FeiDanTest):
    @file_data(case_yml+"\\cardface_result.yaml")
    @unpack

    def test_cardface_case(self,**test_data):
        base_url = test_data.get('url')
        data = test_data.get('data')
        detail = test_data.get('detail')
        headers = test_data.get('header')
        method = test_data.get('method')
        check = test_data.get('check')
        print detail
        if method:
            method = str(method).upper()
            if method == "GET":
                r = requests.get(url=base_url, params=data, headers=headers,verify=False)
            elif method == "POST":
                r = requests.post(url=base_url,json=data,headers=headers,verify=False)
            elif method == "PUT":
                r = requests.put(url=base_url, json=data, headers=headers,verify=False)
            elif method == "DELETE":
                r = requests.delete(url=base_url, json=data, headers=headers,verify=False)
        else:
            r = "CASE WRONG，CASEDATA"
        print r.text
        for c in check:
            self.assertIn(c,r.text)






if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest( CardfaceTestCase("test_cardface_case"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # unittest.main()