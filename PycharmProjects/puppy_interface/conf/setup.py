#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests


class MyTest(unittest.TestCase):
    def login_token(self):
        url = 'http://10.58.122.61:447/api/v1/authz/login'
        param = {'username': 'admin', 'password': 'abc123'}
        r = requests.post(url=url, json=param)
        result = r.json()
        return result['data']



    # @classmethod
    def setUp(self):
        token1 = self.login_token()
        self.domain = 'http://10.58.122.61:447/api/v1/1/'

        #self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.headers = {'content-type': 'application/json',
                        'Authorization': 'Bearer ' + token1}

        print("------------开始执行用例-----------")


    def tearDown(self):
        #print(self.code,self.text)
        print("------------执行用例结束-----------")