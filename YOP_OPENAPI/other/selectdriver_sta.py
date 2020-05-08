#!coding=utf-8
import unittest
import requests
import json
import time
import sys,os
import sqlite3
import datetime
import csv

class SelectDriver_Test(unittest.TestCase): 
    def setUp(self):
        self.domain = 'http://yop.yongche.org/'
        # self.headers = {'content-type':'application/x-www-form-urlencoded'}
        self.headers = {'oauth_consumer_key':'2afdd89f5c6dbdc34542ab04933a091004eba18e2', 
                        'oauth_signature_method':'PLAINTEXT',
                        'oauth_signature':'5sARLGoVkNAPhh5wq1Hl95crWIk',
                        'oauth_timestamp':int(time.time()),
                        'oauth_nonce':uuid.uuid4().hex,
                        'x_auth_mode':'client_auth',
                        'oauth_version':'1.0',
                        'oauth_token': 'eefd533f3c94fc217ffc7c990f441bb10573acbbc',
                        'oauth_token_secret':'157cdbfc4ef5c8598e471df75f7258ce',
                       }

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
                    'car_type_id':'1',
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

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        return result['result']['order_id']

#司机接单

    def test_Driver_Operate(self):
        u'''司机端接单'''
        post_id = self.createorder_post()
        payload = ({'in_coord_type': 'baidu',
                    'is_auto':'0',
                    'method':'accept',
                    'time':'1466065098',
                    'longitude':'116.313985',
                    'distance': '3455',                   
                    'drive_time':'780',
                    'version':'93',                    
                    'latitude':'39.989891',
                    'driver_add_price':'0',
                    'round':'1',
                    'distance':'3455',
                    'provider':'network',                  
                    'driver_add_price':'0',
                    'is_gzip':'1',
                    'round':'1',
                    'order_id':post_id,
                    'batch':'1',
                    'imei':'861726033290352',
                    'x_auth_mode':'client_auth',
                    })

        r = requests.post(('http://testing.driver-api.yongche.org/order/operateOrder'),data=payload,headers=self.headers) 
        print r.text



    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(SelectDriver_Test("test_Driver_Operate"))


    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    #unittest.main()