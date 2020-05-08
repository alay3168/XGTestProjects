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


    def test_check_orderid(self):
        u'''获得单一订单信息'''
        post_id = self.createorder_post()
        r = requests.get('http://yop.yongche.org/v2/order/'+post_id+'?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY')     
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text) 


    def test_order_cost_estimated(self):
        u'''费用预估'''
        payload = ({'city': 'bj',
                  'type': '17',                   
                  'car_type_id':'2',
                  'expect_start_longitude':'116.319322',
                  'expect_start_latitude':'39.987243',
                  'time':self.post_time,
                  'rent_time':'1',
                  'map_type':'1',
                  'expect_end_longitude':'116.485332',
                  'expect_end_latitude':'39.899438',
                  'sms_type':'0',
                  'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                  })

        r = requests.post(self.url('/v2/cost/estimated'), data=payload,headers=self.headers)
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertEqual(result['msg'],'ok')
        self.assertTrue('total_fee' in r.text) 


    def test_nearbyCarCount(self):
        u'''获得附近车辆'''
        r = requests.get(self.url('/v2/driver/nearbyCarCount?lng=39.915175&lat=116.403906&access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)

    def test_service_nightfee(self):
        u'''获得夜间服务费'''
        r = requests.get(self.url('/v2/nightfee?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY&city=bj&car_type_id=2'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)   

    def test_info_airport(self):
        u'''获得机场信息'''
        r = requests.get(self.url('/v2/airport?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY&map_type=1'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_info_train(self):
        u'''获得火车站信息'''
        r = requests.get(self.url('/v2/train?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_info_priceNew(self):
        u'''获得服务价格'''
        r = requests.get(self.url('/v2/priceNew/bj?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY&type=17'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_createOrder_receipt(self):
        u'''开发票'''
        payload = ({'city': u'北京',
              'receipt_title': u'北京车云信息技术有限公司',                   
              'receipt_content':u'打车费',
              'province':u'北京',
              'county':u'海淀区',
              'address':u'北四环中路中国交易技术大厦',
              'postcode':'100086',
              'receipt_user':u'苏昭',
              'receipt_phone':'18611994999',
              'amount':'10',
              'order_id':'6365739068231187551',
              'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'               
              })

        r = requests.post(self.url('/v2/receipt/create'), data=payload)
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)


    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CreateOrder_Test("test_check_orderid"))
    suite.addTest(CreateOrder_Test("test_order_cost_estimated"))
    suite.addTest(CreateOrder_Test("test_nearbyCarCount"))
    suite.addTest(CreateOrder_Test("test_service_nightfee")) 
    suite.addTest(CreateOrder_Test("test_info_airport"))   
    suite.addTest(CreateOrder_Test("test_info_train"))   
    suite.addTest(CreateOrder_Test("test_info_priceNew")) 
    suite.addTest(CreateOrder_Test("test_createOrder_receipt")) 
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)