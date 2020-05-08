#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests


class FeiDanTest(unittest.TestCase):
    def login_token(self):
        url = 'https://feidan.puppyrobot.com/feidan/api/common/login'
        param = {'username': 'super', 'password': 'Abc123'}
        r = requests.post(url=url, json=param,verify=False)
        result = r.json()
        return result['data']

    # @classmethod
    def setUp(self):
        get_token = self.login_token()
        # self.domain = 'https://10.58.122.61:447/api/v1/1/'
        self.heads = {'content-type': 'application/x-www-form-urlencoded',
                        'Authorization': 'Bearer ' + get_token}
        self.headers = {'content-type': 'application/json',
                        'Authorization': 'Bearer ' + get_token}

        print("------------开始执行用例-----------")

    def tearDown(self):

        print("------------执行用例结束-----------")