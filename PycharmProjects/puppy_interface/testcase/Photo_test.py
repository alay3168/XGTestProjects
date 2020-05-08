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
class PhotoTestCase(setup.MyTest):
    @file_data("./Photo_case.yaml")
    def test_Photo_case1(self, **test_data):
        data = test_data.get('data')
        detail =test_data.get('detail')
        check =test_data.get('check')
        print detail
        r = requests.post(self.url('staffs/images'),json=data,headers=self.headers)
        print r.text
        for c in check:
            self.assertIn(c,r.text)

    def test_Photo_case2(self,**test_data):
        data = test_data.get('data')
        detail =test_data.get('detail')
        check =test_data.get('check')
        print detail
        r = requests.post(self.url('staffs/verify_image_exist'),json=data,headers=self.headers)
        print r.text


    # def test_Photo_case3(self, **test_data):
    #     data = test_data.get('data')
    #     detail =test_data.get('detail')
    #     check =test_data.get('check')
    #     print detail
    #     r = requests.post(self.url('most_similar_image'),json=data,headers=self.headers)
    #     print r.text
    #     for c in check:
    #         self.assertIn(c,r.text)

    # def test_Photo_case3(self):
    #     print detail
    #     r = requests.post(self.url('most_similar_image_by_featrue'),json=data,headers=self.headers)
    #     print r.text
    #
    # def test_Photo_case4(self):
    #     print detail
    #     r = requests.post(self.url('verify_image_exist'),json=data,headers=self.headers)
    #     print r.text




    def url(self, path):
        return self.domain + path

if __name__ == '__main__':
    unittest.main()
