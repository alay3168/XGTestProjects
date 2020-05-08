#!coding=utf-8
import unittest
import requests
import json
import time
import sys,os
import sqlite3
import datetime
import csv
import uuid
import random
import string

reload(sys)
sys.setdefaultencoding('utf-8')


class SelectDriver_Test(unittest.TestCase): 
    def setUp(self):
        self.domain = 'http://yop.yongche.org/'
        global time
        self.headers = {'oauth_consumer_key':'2afdd89f5c6dbdc34542ab04933a091004eba18e2', 
             'oauth_signature_method':'PLAINTEXT',
             'oauth_signature':'5sARLGoVkNAPhh5wq1Hl95crWIk',
             'oauth_timestamp':int(time.time()),
             'oauth_nonce':int((time.time())+1000),
             'x_auth_mode':'client_auth',
             'oauth_version':'1.0',
             'oauth_token':'eefd533f3c94fc217ffc7c990f441bb10573acbbc',
             'oauth_token_secret':'157cdbfc4ef5c8598e471df75f7258ce',
             'user_id':'50057992',
             'xmpp_token':'cbb6a3b884f4f88b3a8e3d44c636cbd8',
             'device_id':'50005830'
            }
        # # self.headers = {'content-type':'application/x-www-form-urlencoded',
        #                 'Accept-Encoding':'gzip',
        #                 'Connection':'Keep-Alive',
        #                 'Authorization':'OAuth relam="", %s' % h,
        #                }

        # self.headers = {'Authorization':'OAuth relam="http://testing.driver-api.yongche.org/order/operateOrder"',
        #                 'oauth_consumer_key':'2afdd89f5c6dbdc34542ab04933a091004eba18e2',
        #                 'oauth_token':'eefd533f3c94fc217ffc7c990f441bb10573acbbc',
        #                 'oauth_signature_method':'PLAINTEXT',
        #                 'oauth_signature':'5sARLGoVkNAPhh5wq1Hl95crWIk',
        #                 'oauth_timestamp':int(time.time()),
        #                 'oauth_nonce':int((time.time())+1000),
        #                 'oauth_version':'1.0',
        #                 }

        # self.headers = {'oauth_token':'5b1d253baf0dfffe90090307a1c5b7fa05799c37e',
        #                 'oauth_token_secret':'58e61be18ef1ad61eb1169d593cdbfff',
        #                 }

        # print int(time.time())
        # print int((time.time())+1000)



    # #定义时间变量
    #     time = datetime.datetime.now()
    #     reservation_time = time + datetime.timedelta(hours=24)
    #     self.post_time = reservation_time.strftime("%Y-%m-%d %H:%M:%S")

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
                    'is_asap':'1',
                    'is_face_pay':'0',
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        return result['result']['order_id']
        print r.text


    def  driver_Verify(self):
        
        r = requests.get('http://testing.driver-api.yongche.org/Driver/VerifyCooperaStatus?cellphone=%s&vehicle_number=%s&area_code=%s&version=%s&x_auth_mode=%s&is_gzip=%s&imei=%s'%(16816816810,6666,86,93,'client_auth','true',861726033290352)) 
        result = r.json()
        return result['msg']['password']
    
    def  test_get_accessToken(self):

        password = self.driver_Verify()
        payload = ({'x_auth_username': '16816816810',
                    'x_auth_password': password,                   
                    'device_type':'1',
                    'imei':'861726033290352',
                    })        

        r = requests.post(('http://testing.driver-api.yongche.org/oauth/accessToken'), data=payload)
        result = r.json()
        print r.text
        # return result['msg']['oauth_token']
        # return result['msg']['oauth_token_secret']


#司机接单
    def test_Driver_Operate(self):
        u'''司机端接单'''
        post_id = self.createorder_post()
        payload = ({'in_coord_type': 'baidu',
                    'is_auto':'0',
                    'method':'accept',
                    'longitude':'116.313985',
                    'distance': '3455',                   
                    'drive_time':'0',
                    'version':'93',                    
                    'latitude':'39.989891',
                    'driver_add_price':'0',
                    'round':'1',
                    'provider':'network',                  
                    'driver_add_price':'0',
                    'is_gzip':'true',
                    'round':'1',
                    'order_id':post_id,
                    'batch':'1',
                    'imei':'861726033290352',
                    'x_auth_mode':'client_auth',
                    })

        h = {'oauth_consumer_key':'2afdd89f5c6dbdc34542ab04933a091004eba18e2', 
             'oauth_signature_method':'PLAINTEXT',
             'oauth_signature':'5sARLGoVkNAPhh5wq1Hl95crWIk',
             'oauth_timestamp':int(time.time()),
             'oauth_nonce':uuid.uuid4().hex,
             'x_auth_mode':'client_auth',
             'oauth_version':'1.0',
             'oauth_token':'5b1d253baf0dfffe90090307a1c5b7fa05799c37e',
             'oauth_token_secret':'58e61be18ef1ad61eb1169d593cdbfff',
             'user_id':'50057992',
             'xmpp_token':'cbb6a3b884f4f88b3a8e3d44c636cbd8',
             'device_id':'50005830'
            }



        r = requests.post(('http://testing.driver-api.yongche.org/order/operateOrder'),data=payload,headers={'Authorization': 'OAuth realm="", %s' % h})
        # r = requests.post('http://testing.driver-api.yongche.org/order/operateOrder?oauth_token=5b1d253baf0dfffe90090307a1c5b7fa05799c37e&oauth_token_secret=58e61be18ef1ad61eb1169d593cdbfff', data=payload,headers=self.headers)
#       #r = requests.post(('http://testing.driver-api.yongche.org/order/operateOrder?oauth_consumer_key=2afdd89f5c6dbdc34542ab04933a091004eba18e2&oauth_signature_method=PLAINTEXT&oauth_signature=5sARLGoVkNAPhh5wq1Hl95crWIk&oauth_version=1.0'),data=payload)
        print r.text



    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
    #sys.argv = ['','YOPInterfaceTest.test_3createOrder_afterpay']
    unittest.main()

    