#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2018-8-08
# @Description: HOMEY_API
#****************************************************************

import unittest
import requests
import json
import sys
import yaml
sys.path.append("..")
from common import setup
from common import connect_mysql

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from ddt import ddt,file_data,unpack,data
import os
dir = "testdata"
case_yml = os.path.abspath(os.path.dirname(os.getcwd())) + "\\" + dir

@ddt
class PersonnelTestCase(setup.TokenTest):
    @file_data(case_yml+"\personnel_case.yaml")
    @unpack
    # 新建人员库CASE
    def test_personnel_case1(self,**test_data):
        base_url = test_data.get('url')
        data = test_data.get('data')
        detail =test_data.get('detail')
        check =test_data.get('check')
        method =test_data.get('method')
        print detail
        if method:
            method = str(method).upper()
            if method == "GET":
                r = requests.get(url=base_url, params=data, headers=self.headers,verify=False)
            elif method == "POST":
                r = requests.post(url=base_url,json=data,headers=self.headers,verify=False)
            elif method == "PUT":
                r = requests.put(url=base_url, json=data, headers=self.headers,verify=False)
            elif method == "DELETE":
                r = requests.delete(url=base_url, json=data, headers=self.headers,verify=False)
        else:
            r = "CASE WRONG，CASEDATA"
        # self._testMethodDoc = detail
        # result = r.json()
        for c in check:
            self.assertIn(c, r.text)

    # 修改人员库库名前置

    def Lib_create(self):
        data = ['test1','test2','test3']
        for i in range(len(data)):
            name = data[i]
            params = {'content': name}
            r = requests.post(self.url('staffs/librarys'), json=params,headers=self.headers,verify=False)
            result = r.json()
            Lid = result['data']['id']
            print Lid
            return Lid

    # 修改人员库CASE
    @file_data(case_yml+"\edpersonnel_case.yaml")
    def test_personnel_case3(self,**test_data):
        lib_id = self.Lib_create
        base_url = test_data.get('url')+lib_id
        data = test_data.get('data')
        detail =test_data.get('detail')
        check =test_data.get('check')
        method =test_data.get('method')
        print detail
        print base_url

        if method:
            method = str(method).upper()
            if method == "GET":
                r = requests.get(url=base_url, params=data, headers=self.headers,verify=False)
            elif method == "POST":
                r = requests.post(url=base_url,json=data,headers=self.headers,verify=False)
            elif method == "PUT":
                r = requests.put(url=base_url, json=data, headers=self.headers,verify=False)
            elif method == "DELETE":
                r = requests.delete(url=base_url, json=data, headers=self.headers,verify=False)
        else:
            r = "CASE WRONG，CASEDATA"
        # self._testMethodDoc = detail
        # result = r.json()
        for c in check:
            self.assertIn(c, r.text)



    def url(self, path):
        return self.domain + path



if __name__ == '__main__':

    unittest.main()