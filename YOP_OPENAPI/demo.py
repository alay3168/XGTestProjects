#!coding=utf-8
#****************************************************************
# yop_yidao.py
# Author     : suzhao
# Version    : 1.0
# Date       : 2016-3-29
# Description: YOP接口测试
#****************************************************************
import unittest
import requests
import json
import time
import sys,os
import sqlite3
import datetime
import csv

reload(sys)
sys.setdefaultencoding('utf-8')
my_file = 'E:\\YOP_OPENAPI\\data\\info.csv'
data = csv.reader(file(my_file,'rb'))


class demo(unittest.TestCase):

    def setUp(self):
        self.domain = 'http://yop.yongche.org/'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.send_headers = {'oauth_consumer_key': '2afdd89f5c6dbdc34542ab04933a091004eba18e2',
                              'oauth_token': '734936617d12b016258c79e3580ab2b9057037edd',
                              'oauth_signature_method':'PLAINTEXT',
                              'oauth_signature':'5sARLGoVkNAPhh5wq1Hl95crWIk',
                              'x_auth_mode':'client_auth',
                              'oauth_version':'1.0',
                              'oauth_nonce': '469571399',
                              }
        time = datetime.datetime.now()
        reservation_time = time + datetime.timedelta(hours=1)
        self.post_time = reservation_time.strftime("%Y-%m-%d %H:%M:%S")
          

    def tearDown(self):
          print 'test success'


    def test_demo_info(self):
        u'''5.获取订单司机详细信息'''
        for user in data:
          print(user[2])
          print(user[0])
          url = "http://yop.yongche.org/v2/driver/info?order_id=%s&access_token=%s"%(user[2],user[0])
          print url       
          r = requests.get("http://yop.yongche.org/v2/driver/info?order_id="+ user[2] + "&access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY")
          result =r.json()
          print r.text
          self.assertEqual(r.status_code, 200)
          self.assertEqual(result['msg'],'success')
          self.assertEqual(result['code'], 200)

        #     def url(self, path):
        # return self.domain + path 

if __name__ == '__main__':
     #sys.argv = ['','YOPInterfaceTest.test_driver_location']
    unittest.main()