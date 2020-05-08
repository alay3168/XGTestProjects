#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   log_utility.py.py
@Contact :   xushaohua@puppyrobot.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/3/20 15:57   xushaohua      1.0         None
'''

import logging
from Common import result_folder

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def CreateLoggerFile(filename):
    try:
        fulllogname = result_folder.GetRunDirectory() + "\\" + filename + ".log"
        fh = logging.FileHandler(fulllogname)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [line:%(lineno)d] %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as err:
        logger.debug("Error when creating log file, error message: {}".format(str(err)))


def Log(message):
    logger.debug(message)