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

    def test_CreateOrder_asap_1(self):
        u'''ASAP-马上用车-面付'''
        payload = ({'city': 'bj',
                    'type': '17',                   
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
                    'is_face_pay':'1',
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_CreateOrder_asap_2(self):
        u'''ASAP-马上用车-非面付'''
        payload = ({'city': 'bj',
                    'type': '17',                   
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
                    'is_face_pay':'0',
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()

        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_CreateOrder_appointment_1(self):
        u'''预约用车-面付'''
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
                    'is_face_pay':'1',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_CreateOrder_appointment_2(self):
        u'''预约用车-非面付'''
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
                    'is_face_pay':'0',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_CreateOrder_airport_1(self):
        u'''接机订单-非面付'''
        payload = ({'city': 'bj',
                    'type': '7',                   
                    'car_type_id':'2',
                    'start_position':u'首都机场',
                    'start_address':u'首都机场',
                    'expect_start_longitude':'116.599563',
                    'expect_start_latitude':'40.085493',
                    'end_position':u'红居街',
                    'end_address':u'红居街',
                    'map_type':'1',
                    'expect_end_longitude':'116.30055',
                    'expect_end_latitude':'40.100975',
                    'passenger_name':'test',
                    'passenger_phone':'18910888244',
                    'msg':'客户留言',
                    'is_face_pay':'0',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)


    def test_CreateOrder_airport_2(self):
        u'''接机订单-面付'''
        payload = ({'city': 'bj',
                    'type': '7',                   
                    'car_type_id':'2',
                    'start_position':u'首都机场',
                    'start_address':u'首都机场',
                    'expect_start_longitude':'116.599563',
                    'expect_start_latitude':'40.085493',
                    'end_position':u'红居街',
                    'end_address':u'红居街',
                    'map_type':'1',
                    'expect_end_longitude':'116.30055',
                    'expect_end_latitude':'40.100975',
                    'passenger_name':'test',
                    'passenger_phone':'18910888244',
                    'msg':'客户留言',
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_createOrder_airoff_1(self):
        u'''送机订单-面付'''
        payload = ({'city': 'bj',
                    'type': '8',                   
                    'car_type_id':'2',
                    'start_position':u'中国技术交易大厦',
                    'start_address':u'中国技术交易大厦',
                    'expect_start_longitude':'116.319322',
                    'expect_start_latitude':'39.987243',
                    'end_position':u'首都机场',
                    'end_address':u'首都机场',
                    'map_type':'1',
                    'expect_end_longitude':'116.599563',
                    'expect_end_latitude':'40.085493',
                    'passenger_name':'test',
                    'passenger_phone':'18910888244',
                    'msg':'客户留言',
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_createOrder_airoff_2(self):
        u'''送机订单-非面付'''
        payload = ({'city': 'bj',
                    'type': '8',                   
                    'car_type_id':'2',
                    'start_position':u'中国技术交易大厦',
                    'start_address':u'中国技术交易大厦',
                    'expect_start_longitude':'116.319322',
                    'expect_start_latitude':'39.987243',
                    'end_position':u'首都机场',
                    'end_address':u'首都机场',
                    'map_type':'1',
                    'expect_end_longitude':'116.599563',
                    'expect_end_latitude':'40.085493',
                    'passenger_name':'test',
                    'passenger_phone':'18910888244',
                    'msg':'客户留言',
                    'is_face_pay':'0',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_createOrder_halfday_1(self):
        u'''半日租订单-面付'''
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
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_createOrder_halfday_2(self):
        u'''半日租订单-非面付'''
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
                    'is_face_pay':'0',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)


    def test_createOrder_Allday_1(self):
        u'''日租订单-非面付'''
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
                    'is_face_pay':'0',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)


    def test_createOrder_Allday_2(self):
        u'''日租订单-面付'''
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
                    'is_face_pay':'1',
                    'aircode':'PEK',
                    'time':self.post_time,
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)






    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreateOrder_Test("test_CreateOrder_asap_1"))
    suite.addTest(CreateOrder_Test("test_CreateOrder_asap_2"))
    suite.addTest(CreateOrder_Test("test_CreateOrder_appointment_1"))
    suite.addTest(CreateOrder_Test("test_CreateOrder_appointment_2"))
    suite.addTest(CreateOrder_Test("test_CreateOrder_airport_1"))
    suite.addTest(CreateOrder_Test("test_CreateOrder_airport_2"))
    suite.addTest(CreateOrder_Test("test_createOrder_airoff_1"))
    suite.addTest(CreateOrder_Test("test_createOrder_airoff_2"))
    suite.addTest(CreateOrder_Test("test_createOrder_halfday_1"))
    suite.addTest(CreateOrder_Test("test_createOrder_halfday_2"))
    suite.addTest(CreateOrder_Test("test_createOrder_Allday_1"))
    suite.addTest(CreateOrder_Test("test_createOrder_Allday_2"))





    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    #unittest.main()