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


#创建本地一口价临时订单
    def createpackage_post1(self):

        payload = ({'city': 'bj',
                    'type': '7',                   
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
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('v2/ctrip/packagefee'), data=payload,headers=self.headers)
        print r.text
        result = r.json()
        return result['result']['order_id']

    def createpackage_post2(self):

        payload = ({'city': 'bj',
                    'type': '12',                   
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
                    'is_face_pay':'1',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'ut1F44TuZiNCxGl9QqLv4WyajMlyDq8myLPOkfvP', 
                    })

        r = requests.post(self.url('v2/ctrip/packagefee'), data=payload,headers=self.headers)
        result = r.json()
        return result['result']['order_id']

    def createpackage_post3(self):

        payload = ({'city': 'bj',
                    'type': '7',                   
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
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'ut1F44TuZiNCxGl9QqLv4WyajMlyDq8myLPOkfvP', 
                    })

        r = requests.post(self.url('v2/ctrip/packagefee'), data=payload,headers=self.headers)
        print r.text
        result = r.json()
        return result['result']['order_id']


    def test_createpackage_local_airport1(self):
        u'''1.本地一口价-接送机'''
        order_id = self.createpackage_post1()
        payload = ({'city': 'bj',
                    'type': '7',                   
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
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    'order_id':order_id,
                    })

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)     



    def test_createpackage_local_airport2(self):
        u'''2.新一口价-接送机'''
        order_id = self.createpackage_post3()
        payload = ({'city': 'bj',
                    'type': '7',                   
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
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'ut1F44TuZiNCxGl9QqLv4WyajMlyDq8myLPOkfvP', 
                    'order_id':order_id,
                    })

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)  

    def test_createpackage_local_allday1(self):
        u'''本地一口价-日租半日租'''
        order_id = self.createpackage_post2()
        payload = ({'city': 'bj',
                    'type': '12',                   
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
                    'is_face_pay':'1',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'ut1F44TuZiNCxGl9QqLv4WyajMlyDq8myLPOkfvP', 
                    'order_id':order_id,
                    })

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_createpackage_local_allday2(self):
        u'''新一口价-日租半日租'''
        order_id = self.createpackage_post2()
        payload = ({'city': 'bj',
                    'type': '11',                   
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
                    'is_face_pay':'1',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    'day_rent_new_fixed_price':'1',
                     'appoint_price':'325',
                    })

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreateOrder_Test("test_createpackage_local_airport1"))
    suite.addTest(CreateOrder_Test("test_createpackage_local_airport2"))
    suite.addTest(CreateOrder_Test("test_createpackage_local_allday1"))
    suite.addTest(CreateOrder_Test("test_createpackage_local_allday2"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    #unittest.main()

