#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2018-8-08
# @Description: 智能监控平台API
# ****************************************************************


import unittest
import requests
import json
import sys
import yaml

sys.path.append("..")
from conf import setup
from ddt import ddt, file_data

@ddt
class AlarmTestCase(setup.MyTest):

    def test_Alarm_case1(self):
        r = requests.get(self.url('alarms/events'),headers=self.headers)
        print r.text
        self.code = r.status_code
        self.text = r.text
        self.assertEqual(self.code, 200)
        self.assertTrue('id' in self.text)

    @file_data("./Alarms_case.yaml")
    def test_Alarm_case2(self, **test_data):
        url = test_data.get('url')
        data = test_data.get('data')
        detail =test_data.get('detail')
        check =test_data.get('check')
        method = test_data.get('method')
        print detail
        if method:
            method = str(method).upper()
            if  method == "GET":
                r = requests.get(url=url,params=data,headers=self.headers)
            elif method == "POST":
                r = requests.get(url=url,json=data,headers=self.headers)
            elif method == "PUT":
                r = requests.get(url=url, json=data, headers=self.headers)
            elif method == "DELETE":
                r = requests.delete(url=url,json=data,headers=self.headers)
        else:
            r = "CASE WRONG，CASEDATA"
        # r = requests.put(self.url('alarms/events/confs'),json=data,headers=self.headers)
        print r.text
        for c in check:
            self.assertIn(c,r.text)

    def test_Alarm_case3(self):
        u'''获取事件规则配置信息'''
        r = requests.get(self.url('alarms/events/confs'),headers=self.headers)
        print r.text

    @file_data("./uuid_case.yaml")
    def test_Alarm_case4(self, **test_data):
        u'''根据事件id添加摄像机'''
        data = test_data.get('data')
        ids = test_data.get('ids')
        check = test_data.get('check')
        r = requests.put(self.url('alarms/events/%s/cameras'%(ids)),json =data,headers=self.headers)
        print r.text

    def test_Alarm_case5(self):
        u'''根据摄像机uuid查找ids'''
        uuid = "22CDE2D0-475B-4C76-BB27-79F6021CC9BC"
        r = requests.get(self.url('alarms/cameras/%s/events'%(uuid)), headers=self.headers)
        print r.text
        self.code = r.status_code
        self.text = r.text
        res = r.json()
        self.assertEqual(self.code, 200)
        self.assertEqual(res['data'],['1','2','3','4','5','6'])

    @file_data("./uuid_case.yaml")
    def test_Alarm_case6(self, **test_data):
        u'''根据事件id删除摄像机'''
        data = test_data.get('data')
        ids = test_data.get('ids')
        check = test_data.get('check')
        r = requests.post(self.url('alarms/events/%s/del_cameras'%(ids)),json =data,headers=self.headers)
        print r.text

    def test_Alarm_case7(self):
        u'''根据摄像机uuid查找ids'''
        uuid = "22CDE2D0-475B-4C76-BB27-79F6021CC9BC"
        r = requests.get(self.url('alarms/cameras/%s/events'%(uuid)), headers=self.headers)
        print r.text
        self.code = r.status_code
        self.text = r.text
        res = r.json()
        self.assertEqual(self.code, 200)
        self.assertEqual(res['data'],[])
















    def url(self, path):
        return self.domain + path

if __name__ == '__main__':
    unittest.main()

