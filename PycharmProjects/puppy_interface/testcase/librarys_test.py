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
import json
import sys
import yaml
sys.path.append("..")
from conf import setup
from ddt import ddt,file_data

@ddt
class LibraryTestCase(setup.MyTest):
    @file_data("./librarys_case.yaml")
    def test_Library_case1(self,**test_data):
        data = test_data.get('data')
        detail =test_data.get('detail')
        check =test_data.get('check')
        print detail
        # self._testMethodDoc = detail
        r = requests.post(self.url('staffs/librarys'),json=data,headers=self.headers)
        print r.text
        result = r.json()

        for c in check:
            if c == u'测试TestA001':
                Library_id = result['data']['id']
                print Library_id
            else:
                self.assertIn(c, r.text)

    def Library_create(self):
        params = {'content': u'自动化测试A'}
        r = requests.post(self.url('staffs/librarys'), json=params, headers=self.headers)
        result = r.json()
        Lid = result['data']['id']
        return Lid
    #
    #
    # # def test_Library_case2(self):
    # #     u'''查看人员库列表'''
    # #     Lid = self.Library_create()
    # #     r = requests.get(self.url('staffs/librarys'),headers=self.headers)
    # #     result = r.json()
    # #     self.code = r.status_code
    # #     self.text = r.text
    # #     self.assertEqual(self.code,200)
    # #     self.assertIn(Lid,self.text)
    #
    # @file_data("./librarys_case.yaml")
    # def test_Library_case3(self,**test_data):
    #     cid = self.Library_create()
    #     data = test_data.get('data')
    #     check =test_data.get('check')
    #     detail =test_data.get('detail')
    #     print detail
    #     r = requests.put(self.url('staffs/librarys/13'),json=data,headers=self.headers)
    #     print r.text
        # result = r.json()
        # self.code = r.status_code
        # self.text = r.text
        # for c in check:
        #     if c == u"测试TestA001":
        #         self.assertEqual(result['errMessage'],u'库名称已存在')
        #     else:
        #         self.assertIn(c,r.text)

    # def test_Library_case4(self):
    #     lib_id = self.Librany_create()
    #     r = requests.delete(self.url('librarys/'+lib_id), headers=self.headers)
    #     print r.text
    #     result = r.json()
    #     self.code = r.status_code
    #     self.text = r.text
    #     self.assertEqual(self.code, 200)
    #     self.assertEqual(result['errCode'],0)

    # def test_Library_case5(self):
    #     u'''删除人员库'''
    #     r = requests.post(self.url('batch_delete_librarys'),headers=self.headers)
    #     print r.text
    #     result = r.json()
    #     self.code = r.status_code
    #     self.text = r.text
    #     self.assertEqual(self.code, 200)
    #     self.assertEqual(result['errCode'],0)






    def url(self, path):
        return self.domain + path




if __name__ == '__main__':

    unittest.main()