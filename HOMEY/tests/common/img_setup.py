#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time


class ImageTest(unittest.TestCase):

    def setUp(self):
        self.domain = 'http://10.58.150.6:29004/api/v1/imagelogs'
        self.headers = {'content-type': 'application/x-www-form-urlencoded',
                        'Connection': 'Keep-Alive'
                        }

        now = time.time()
        print now


        # print("------------开始执行用例-----------")

    def tearDown(self):
        pass

        #print(self.code,self.text)
        # print("------------执行用例结束-----------")