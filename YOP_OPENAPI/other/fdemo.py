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
#引入CSV文件
my_file = 'E:\\YOP_OPENAPI\\data\\cartype.csv'
data = csv.reader(file(my_file,'rb'))
for row in data:
    print ', '.join(row)

class YOPInterfaceTest(unittest.TestCase):

    def setUp(self):
        self.domain = 'http://yop.yongche.org/'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        time = datetime.datetime.now()
        reservation_time = time + datetime.timedelta(hours=1)
        self.post_time = reservation_time.strftime("%Y-%m-%d %H:%M:%S")


    def tearDown(self):
        print 'test success'


    # def test_order_costestimated(self):
    #     u'''费用预估'''
    #     params = ({'city': 'bj',
    #               'type': '7',                   
    #               'car_type_id':'2',
    #               'aircode':'PEK',
    #               'expect_start_longitude':'116.319322',
    #               'expect_start_latitude':'39.987243',
    #               'time':self.post_time,
    #               'rent_time':'1',
    #               'map_type':'1',
    #               'expect_end_longitude':'116.485332',
    #               'expect_end_latitude':'39.899438',
    #               'sms_type':'0',
    #               'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
    #               })

    #     r = requests.post(self.url('/v2/cost/estimated'), data=params,headers=self.headers)
    #     result = r.json()
    #     print r.text
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(result['code'], 200)
    #     self.assertEqual(result['msg'],'ok')


    def test_1createOrder_isamap(self):
        u'''1.创建订单-随叫随到-面付'''
        payload = ({'city': 'bj',
          'type': '1',                   
          'car_type_id':row[0],
          'start_position':u'中关村购物中心',
          'start_address':u'中关村购物中心b座',
          'expect_start_longitude':'116.319322',
          'expect_start_latitude':'39.987243',
          'end_position':u'九龙山',
          'end_address':u'龙乐山地铁站',
          'map_type':'1',
          'expect_end_longitude':'116.485332',
          'expect_end_latitude':'39.899438',
          'passenger_name':'test',
          'passenger_phone':'18910888244',
          'passenger_number':'2',
          'msg':'客户留言',
          'is_asap':'1',
          'is_face_pay':'1',
          'sms_type':'0',
          'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
          })
        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)    
        result = r.json()
        print r.text
        print result['result']['order_id']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)
        



    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
   
    unittest.main()