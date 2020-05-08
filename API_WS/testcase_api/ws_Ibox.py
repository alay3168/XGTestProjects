#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2019-8-28
# @Description: FEIDAN_API
#****************************************************************

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import unittest
import json
import sys
import time
sys.path.append("..")
from common import conf
from ddt import ddt,file_data,unpack,data
import os


case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../testdata"))

@ddt
class AlarmsCase(conf.IboxTest):

    def on_message(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")
    @file_data(case_yml + "/wslogin.yaml")
    def test_on_open(self, **test_data):
        base_url = test_data.get('url')
        data = test_data.get('data')
        detail = test_data.get('detail')
        check = test_data.get('check')
        print detail

        ws.send(json.dumps(data))
        time.sleep(1)



        # for c in check:
        #     for k,v in c.items():
        #         self.assertEqual(rec.get(k),v)


if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://10.58.122.215:8000",
                                on_message= on_message,
                                on_error= on_error,
                                on_close= on_close)
    ws.on_open = test_on_open
    ws.run_forever()
    # 构造测试集
    suite = unittest.TestSuite()

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # unittest.main()