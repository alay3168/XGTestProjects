#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   result_folder.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/20 15:59   xushaohua      1.0         None
'''

import os


def GetRunDirectory():
    allRunFolders = [fd for fd in os.listdir(".") if os.path.isdir(fd) and fd.startswith("TestRun")]
    latestFolder = max(allRunFolders, key=os.path.getmtime)
    return latestFolder