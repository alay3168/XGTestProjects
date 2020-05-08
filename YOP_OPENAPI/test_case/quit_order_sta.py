#!coding=utf-8
import unittest
import requests
import json
import time
import sys,os
import sqlite3
import datetime
import csv


class CreateOrder_Test(unittest.TestCase): 
    def setUp(self):
        self.domain = 'http://yop.yongche.org/'
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
    #定义时间变量
        time = datetime.datetime.now()
        reservation_time = time + datetime.timedelta(hours=24)
        self.post_time = reservation_time.strftime("%Y-%m-%d %H:%M:%S")

    def tearDown(self):
        print 'test success'


#创建订单
    def createorder_post(self):

        payload = ({'city': 'bj',
                    'type': '1',                   
                    'car_type_id':'2',
                    'start_position':u'中国技术交易大厦',
                    'start_address':u'中国技术交易大厦',
                    'expect_start_longitude':'116.319322',
                    'expect_start_latitude':'39.987243',
                    'end_position':u'红居街',
                    'end_address':u'红居街',
                    'map_type':'1',
                    'expect_end_longitude':'116.30055',
                    'expect_end_latitude':'40.100975',
                    'passenger_name':'test',
                    'passenger_phone':'18910888244',
                    'msg':'客户留言',
                    'is_asap':'0',
                    'is_face_pay':'0',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        return result['result']['order_id']

    def test_quit_order(self):
        u'''取消订单'''
        post_id = self.createorder_post()
        payload = ({'reason_id': '61',
                   'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'
                   })
        r = requests.delete('http://yop.yongche.org/v2/order/'+post_id, params=payload)
        #result = json.loads(r)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('OK' in r.text)
        self.assertTrue('200' in r.text)






    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
    #sys.argv = ['','YOPInterfaceTest.test_3createOrder_afterpay']
    unittest.main()