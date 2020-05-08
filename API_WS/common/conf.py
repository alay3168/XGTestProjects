#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import unittest
import json
import sys
sys.path.append("..")

# WS = None
class IboxTest(unittest.TestCase):
    # def get_token(self):
        # url = 'ws://10.58.122.215:8000'
        # data = {"Method":"Login",
        #          "Page":"Login",
        #          "Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}
        # ws = websocket.create_connection(url)
        # ws.send(json.dumps(data))
        # r = ws.recv()
        # result = json.loads(r)
        # print result['Message']
        # return result['Message']

    # def __init__(self,*args,**kwargs):
    #     # global WS
    #     unittest.TestCase.__init__(self, *args, **kwargs)
    #     # if WS is not None:
    #     #     self.ws = WS
    #     #     return
    #     url = 'ws://10.58.122.205:8000'
    #
    #     data = {"Method":"Login",
    #              "Page":"Login",
    #              "Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}
    #     self.ws = websocket.create_connection(url)
    #     self.ws.send(json.dumps(data))
    #     result = self.ws.recv()
    #     print("Received '%s'" % result)
     @classmethod
    def setUp(self):
            url = 'ws://10.58.122.205:8000'

            data = {"Method":"Login",
                     "Page":"Login",
                     "Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}
            self.ws = websocket.create_connection(url)
            self.ws.send(json.dumps(data))
            result = self.ws.recv()
            print("Received '%s'" % result)
        # login_token = self.get_token()
        # url = 'ws://10.58.122.215:8000'
        # self.url = url +'%s %s'%('/token?',login_token )
        # self.ws = websocket.create_connection(self.url)
        # result = self.ws.recv()
        # print("Received '%s'" % result)
            print("------------连接WebSocket成功-----------")

    def tearDown(self):

        print("------------执行用例结束-----------")
