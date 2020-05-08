#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   33.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/18 12:51   xushaohua      1.0         None
'''


class BasePage(object):
    # webdriver instance
    def __init__(self, driver):
        self.driver = driver