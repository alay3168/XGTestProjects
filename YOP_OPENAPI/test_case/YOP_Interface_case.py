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
my_file = 'E:\\YOP_OPENAPI\\data\\info.csv'
data = csv.reader(file(my_file,'rb'))
for user in data:
    print user[0]
    print user[1]
    print user[2]
    print user[3]
    print user[4]

class YOPInterfaceTest(unittest.TestCase):

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


    #创建订单
    def createorder_get(self):
        payload = ({'city': 'bj',
                    'type': '1',                   
                    'car_type_id':'2',
                    'start_position':u'中关村购物中心',
                    'start_address':u'中关村购物中心b座',
                    'expect_start_longitude':'116.319322',
                    'expect_start_latitude':'39.987243',
                    'rent_time':'1',
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
                    'is_face_pay':'0',
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    })

        r = requests.post(self.url('/v2/order'), data=payload,headers=self.headers)
        result = r.json()
        #print(type(result['result']['order_id']))
        #print result['result']['order_id']
        # self.assertTrue(result['code'], '200')
        # self.assertTrue('order_id' in r.text)
        # print result['result']['order_id']
        # id = str(result['result']['order_id'])
        return result['result']['order_id']
        # print (type(id))  
        # print id 


    def test_1createOrder_isamap(self):
        u'''1.创建订单-随叫随到-面付'''
        payload = ({'city': 'bj',
          'type': '1',                   
          'car_type_id':'1',
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
        #print result['result']['order_id']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)

    def test_2createOrder_eservation(self):
        u'''2.创建订单-预约-非面付'''
        payload = ({'city': 'bj',
              'type': '1',                   
              'car_type_id':'1',
              'start_position':u'中关村购物中心',
              'start_address':u'中关村购物中心b座',
              'expect_start_longitude':'116.319322',
              'expect_start_latitude':'39.987243',
              'time':self.post_time,
              'end_position':u'九龙山',
              'end_address':u'龙乐山地铁站',
              'map_type':'1',
              'expect_end_longitude':'116.485332',
              'expect_end_latitude':'39.899438',
              'passenger_name':'test',
              'passenger_phone':'18910888244',
              'passenger_number':'2',
              'msg':'客户留言',
              'is_asap':'0',
              'is_face_pay':'0',
              'sms_type':'0',
              'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
              })

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)    

    def test_3createOrder_afterpay(self):
        u'''3.创建订单-预约-面付'''
        payload = ({'city': 'bj',
                'type': '1',                   
                'car_type_id':'1',
                'start_position':u'中关村购物中心',
                'start_address':u'中关村购物中心b座',
                'expect_start_longitude':'116.319322',
                'expect_start_latitude':'39.987243',
                'time':self.post_time,
                'end_position':u'九龙山',
                'end_address':u'龙乐山地铁站',
                'map_type':'1',
                'expect_end_longitude':'116.485332',
                'expect_end_latitude':'39.899438',
                'passenger_name':'test',
                'passenger_phone':'18910888244',
                'passenger_number':'2',
                'msg':'客户留言',
                'is_asap':'0',
                'is_face_pay':'1',
                'sms_type':'0',
                'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                })

        r = requests.post(self.url('/v2/order'), data=payload)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)  

    def test_4packagefee(self):
        u'''4.创建携程套餐包'''
        payload = ({'city': 'bj',
                  'type': '1',                   
                  'car_type_id':'1',
                  'start_position':u'中关村购物中心',
                  'start_address':u'中关村购物中心b座',
                  'expect_start_longitude':'116.319322',
                  'expect_start_latitude':'39.987243',
                  'time':self.post_time,
                  'rent_time':'1',
                  'end_position':u'九龙山',
                  'end_address':u'龙乐山地铁站',
                  'map_type':'1',
                  'expect_end_longitude':'116.485332',
                  'expect_end_latitude':'39.899438',
                  'passenger_name':'test',
                  'passenger_phone':'18910888244',
                  'passenger_number':'2',
                  'msg':'客户留言',
                  'is_asap':'0',
                  'is_face_pay':'1',
                  'sms_type':'0',
                  'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                  'third_party_coupon':'2'
                  })

        r = requests.post(self.url('v2/ctrip/packagefee'), data=payload)
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text)  

     # def test_Driver_OperateOrder(self):
     #      u'''司机端接单'''
     #      payload = ({'in_coord_type': 'baidu',
     #                'distance': '0',                   
     #                'drive_time':'0',
     #                'longitude':'116.313888',
     #                'latitude':'39.989962',
     #                'time':'1460015446',
     #                'provider':'network',                  
     #                'driver_add_price':'0',
     #                'is_gzip':'true',
     #                'is_auto':'0',
     #                'imei':'863361021694551',
     #                'x_auth_mode':'client_auth',
     #                'order_id':'2005771554',
     #                'method':'accept',
     #                })

     #      r = requests.post(('http://testing.d.yongche.org/order/operateOrder'), data=payload,headers=self.send_headers) #, headers=self.send_headers
     #      print r.text

    def test_5Drinr_info(self):
        u'''5.获取订单司机详细信息'''
        # for user in data:
        #     print  user[2]
        #     print user[0]
        r = requests.get('http://yop.yongche.org/v2/driver/info?order_id=%s&access_token=%s'%(user[3],user[0]))
        #print r.text
        result =r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)

    def test_6del_order(self):
        u'''6.取消订单'''
        post_id = self.createorder_get()
        payload = ({'reason_id': '61',
                   'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'
                   })
        r = requests.delete('http://yop.yongche.org/v2/order/'+post_id, data=payload)
        #print r.text
        #result = json.loads(r)
        self.assertEqual(r.status_code, 200)
        #self.assertEqual(result['msg'],'ok')
        #self.assertEqual(result['code'], 200)
        self.assertTrue('OK' in r.text)
        self.assertTrue('200' in r.text) 

    def test_7decisionDriver(self):
        u'''7.乘客选择司机'''
        # for user in data:
        #     print user[1]
        payload = ({'order_id': user[1],          
                'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                'driver_id':'50057150'
                })
        r = requests.post(self.url('/v2/driver/decisionDriver'), data=payload)    
        result = r.json()
        # self.assertEqual(r.status_code, 200)
        # self.assertEqual(result['code'], 200)

    def test_8third_party_coupon(self):
        u'''8.支付宝''' 
        # for user in data:
        #     print user[3]
        r = requests.get('http://yop.yongche.org/v2/payCash?amount=50&access_token=%s&order_id=%s'%(user[0],user[3]))
        #print r.status_code
        #print r.text          
        result = r.json()
        self.assertEqual(result['code'], 200)
        self.assertEqual(result['msg'], 'success')

  #待修改
    def test_9_1b_createOrder_ordercalculate(self):
        u'''9.查询订单费用详情'''  
        # for user in data:
        #     print user[3]       
        r = requests.get('http://yop.yongche.org/v2/order/calculate/%s?access_token=%s'%(user[3],user[0]))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text) 

    def test_9_1check_orderid(self):
        u'''10.获得单一订单信息'''
        post_id = self.createorder_get()
        r = requests.get('http://yop.yongche.org/v2/order/'+post_id+'?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY')     
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)
        self.assertTrue('order_id' in r.text) 

    def test_9_2order_cost_estimated(self):
        u'''11.费用预估'''
        payload = ({'city': 'bj',
                  'type': '1',                   
                  'car_type_id':'1',
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
          #self.assertTrue('order_id' in r.text)
  #待修改
    def test_9_3driver_location(self):
        u'''12.获取司机位置'''
        # for user in data:
        #     print(user[2])
        #     print(user[0])
        r = requests.get('http://yop.yongche.org/v2/driver/location?order_id=%s&access_token=%s'%(user[2],user[0]))     
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)


    def test_9_4service_get(self):
        u'''13.可用服务'''
        r = requests.get(self.url('/v2/service?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_9_5service_get_new(self):
        u'''14.新服务价格'''
        r = requests.get(self.url('/v2/priceNew/bj?type=1&access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_9_6service_get_old(self):
        u'''15.老服务价格'''
        r = requests.get(self.url('/v2/price/bj?type=1&access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_9_7nearbyCarCount(self):
        u'''16.获得附近车辆'''
        r = requests.get(self.url('/v2/driver/nearbyCarCount?lng=39.987243&lat=116.319322=&access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)

    def test_9_8service_nightfee(self):
        u'''17.夜间服务费'''
        r = requests.get(self.url('/v2/nightfee?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY&city=bj&car_type_id=1'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)   

    def test_9_9info_airport(self):
        u'''18.获得机场信息'''
        r = requests.get(self.url('/v2/airport?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY&map_type=1'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_a_info_train(self):
        u'''19.获得火车站信息'''
        r = requests.get(self.url('/v2/train?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)

    def test_b_createOrder_receipt(self):
        u'''20.开发票'''
        payload = ({'city': u'北京',
              'receipt_title': u'北京车云信息技术有限公司',                   
              'receipt_content':u'打车费',
              'province':u'北京',
              'county':u'海淀区',
              'address':u'北四环中路中国交易技术大厦',
              'postcode':'100086',
              'receipt_user':u'苏昭',
              'receipt_phone':'18611994999',
              'amount':'1000',
              'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'               
              })

        r = requests.post(self.url('/v2/receipt/create'), data=payload)
        result = r.json()
        #print r.text
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)

    def test_c_put_order(self):
        u'''21.修改订单'''        
        payload = ({'passenger_name': u'张三',
         'passenger_phone':'18710101001',
         'passenger_number':'3',
         'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY',
         'coupon_name':u'易到用车优惠券'

         })
        r = requests.put('http://yop.yongche.org/v2/order/'+user[3], data=payload)
        #print r.text
        result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'OK')
        self.assertEqual(result['code'], 200)
        self.assertTrue('OK' in r.text)
        self.assertTrue('200' in r.text) 
          
     # def test_get_commentTag(self):
     #      '''23.获得评价标签'''
     #      r = requests.get(self.url('/v2/commentTag?access_token=NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY'))
     #      #result = r.json()
     #      print r.text
     #      self.assertEqual(r.status_code, 200)
     #      self.assertEqual(result['msg'],'OK')
     #      self.assertEqual(result['code'], 200)


    def test_d_post_comment(self):
        u'''22.提交评价'''
        payload = ({'content': u'好评',
                    'score':'5',
                    'comment_tag_id':'1,3',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY',
                    'order_id':user[3]
                  })
        r = requests.post('http://yop.yongche.org/v2/comment', data=payload)
        #print r.text
        self.assertEqual(r.status_code, 200)
          #self.assertEqual(result['msg'],'ok')
          #self.assertEqual(result['code'], 200)
          # self.assertTrue('OK' in r.text)
          # self.assertTrue('200' in r.text) 


    def test_e_createOrder_newprice_halfday_check(self):
        u'''23.新一口价-半日租-校验预估阈值'''
        payload = ({'city': 'bj',
                    'type': '11',                   
                    'car_type_id':'1',
                    'start_position':u'中关村购物中心',
                    'start_address':u'中关村购物中心b座',
                    'expect_start_longitude':'116.319322',
                    'expect_start_latitude':'39.987243',
                    'time':self.post_time,
                    'rent_time':'1',
                    'end_position':u'九龙山',
                    'end_address':u'龙乐山地铁站',
                    'map_type':'1',
                    'expect_end_longitude':'116.485332',
                    'expect_end_latitude':'39.899438',
                    'passenger_name':'test',
                    'passenger_phone':'18910888244',
                    'passenger_number':'2',
                    'msg':'客户留言',
                    'is_asap':'0',
                    'is_face_pay':'1',
                    'sms_type':'0',
                    'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY', 
                    'third_party_coupon':'2',
                    'appoint_price':'250',
                    'day_rent_new_fixed_price':'1'
              })

        r = requests.post(self.url('/v2/order'), data=payload)
        # print r.status_code
        # print r.text          
        result = r.json()
        self.assertEqual(result['code'], 530)

    def test_f_createOrder_newprice_Oneday_check(self):
        u'''24.新一口价-日租-校验预估阈值'''
        payload = ({'city': 'bj',
              'type': '12',                   
              'car_type_id':'1',
              'start_position':u'中关村购物中心',
              'start_address':u'中关村购物中心b座',
              'expect_start_longitude':'116.319322',
              'expect_start_latitude':'39.987243',
              'time':self.post_time,
              'rent_time':'1',
              'end_position':u'九龙山',
              'end_address':u'龙乐山地铁站',
              'map_type':'1',
              'expect_end_longitude':'116.485332',
              'expect_end_latitude':'39.899438',
              'passenger_name':'test',
              'passenger_phone':'18910888244',
              'passenger_number':'2',
              'msg':'客户留言',
              'is_asap':'0',
              'is_face_pay':'1',
              'sms_type':'0',
              'access_token':'NXyX5pie5jl8prVgrO6YBSaABq9HdxXM3uXgSUIY',                     
              'appoint_price':'510',
              'day_rent_new_fixed_price':'1'
              })

        r = requests.post(self.url('/v2/order'), data=payload)         
        result = r.json()
        self.assertEqual(result['code'], 200)


    def test_zgetSelectDriver(self):
        u'''25.获取司机列表'''
        # for user in data:
        #     print user[1]          
        r = requests.get('http://yop.yongche.org//v2/driver/getSelectDriver?access_token=%s&order_id=%s'%(user[0],user[2]))
        result =r.json
        #print r.text
        self.assertEqual(r.status_code, 200)
        #self.assertEqual(result['code'], 200)
        self.assertTrue('carlist'in r.text)

    def test_zDrinr_orderTrack(self):
        u'''26.订单行驶轨迹'''
        r = requests.get('http://yop.yongche.org/v2/driver/orderTrack?order_id=%s&access_token=%s'%(user[3],user[0]))
        #print r.text
        result =r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['msg'],'success')
        self.assertEqual(result['code'], 200)
        self.assertTrue('result'in r.text)


     





    def url(self, path):
        return self.domain + path


if __name__ == '__main__':
    #sys.argv = ['','YOPInterfaceTest.test_3createOrder_afterpay']
    unittest.main()