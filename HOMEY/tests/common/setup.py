#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TokenTest(unittest.TestCase):
    def login_token(self):
        url = 'https://10.58.122.61:447/api/v1/authz/login'
        param = {'username': 'admin', 'password': 'abc123'}
        r = requests.post(url=url, json=param,verify=False)
        result = r.json()
        return result['data']



    # @classmethod
    def setUp(self):
        get_token = self.login_token()
        self.domain = 'https://10.58.122.61:447/api/v1/1/'

        #self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.headers = {'content-type': 'application/json',
                        'Authorization': 'Bearer ' + get_token}

        print("------------开始执行用例-----------")

    def tearDown(self):
        #print(self.code,self.text)
        print("------------执行用例结束-----------")