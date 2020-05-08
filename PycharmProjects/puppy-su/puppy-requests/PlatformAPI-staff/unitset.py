#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @auther:suzhao

import unittest


class MyTest(unittest.TestCase):
    def setUp(self):
        self.domain = 'http://10.58.122.61/api/v1/staffs/'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}


    def tearDown(self):
        print(self.code,self.text)