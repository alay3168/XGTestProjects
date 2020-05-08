#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @auther:suzhao

import unittest
import requests
import sys
sys.path.append("..")
from data_fixture import request_data
import unitset



class StaffTestCase(unitset.MyTest):


    def test_staff_register(self):
        u'''1.注册人员-新人员注册-正常注册'''

        r = requests.post(self.url('peoples'),data = request_data.register_data1(),headers = self.headers)
        self.code = r.status_code
        self.text = r.text
        # result = r.json()
        # self.assertEqual(self.code,200)
        # self.assertEqual(result['code'],200)
        # self.assertTrue(''in self.text)

    #def test_staff_register2(self):



    # def test_staff_get(self):
    #     r = requests.get(self.url('peoples/1'),headers = self.headers))
    #     self.code = r.status_code
    #     self.text = r.text





#self.assertEqual(True, False)








    def url(self, path):
        return self.domain + path



if __name__ == '__main__':
    unittest.main()

