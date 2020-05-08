#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run.py    
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/18 19:01   xushaohua      1.0         None
'''
import unittest
from BoxWebAutoTest.case.TestLoginPage import Test_LoginPage


if __name__ == '__main__':
    # suite = unittest.TestSuite
    # loader = unittest.TestLoader()
    # unittest.TestLoader().loadTestsFromTestCase(Test_LoginPage)
    #
    # unittest.TestLoader().loadTestsFromTestCase(Test_LoginPage)  # 测试用例类名直接传入
    suite=unittest.TestSuite
    suite.addTest(Test_LoginPage("test_LoginPage_Normal"))
    suite.addTest(Test_LoginPage("test_LoginPage_Wrong_pwd"))

    runner = unittest.TextTestRunner()
    runner.run(suite)