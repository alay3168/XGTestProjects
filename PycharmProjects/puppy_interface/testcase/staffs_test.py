#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2018-8-08
# @Description: 智能监控平台API
#****************************************************************


import unittest
import requests
import json
import sys
import yaml
sys.path.append("..")
from conf import setup
from ddt import ddt,file_data

@ddt
class StasffsTestCase(setup.MyTest):
    def test_Staff_case1(self,**test_data):








if __name__ == '__main__':
    unittest.main()
