#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import wmi
c = wmi.WMI(namespace='root\WMI')

a = c.WmiMonitorBrightnessMethods()[0]
num = 0
time_sleep = 60
while True:
    if num<100:
        a.WmiSetBrightness(Brightness=100, Timeout=500)
        time.sleep(time_sleep)
        num +=10
    else:
        num =0
