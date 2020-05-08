#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     :
# @Version    : 1.0
# @Date       :
# @Description: Momitor
#****************************************************************

import telnetlib
import time
from influxdb import InfluxDBClient
import threading
import logging
import traceback

LOGGER = logging.getLogger("monitor")

def pfloat(p):
    return float(p.replace('%', ''))

def do_telnet(Host, username, password, finish, cmds):
    tn = telnetlib.Telnet(Host, port=23, timeout=60)
    # 输入登录用户名
    tn.read_until(b'login:')
    tn.write(username)

    # 输入登录密码
    tn.read_until(b'Password:')
    tn.write(password)

    # 登录完毕后执行命令
    tn.read_until(finish)
    tn.write(cmds)
    # for command in cmds:
    #     result = tn.write('%s \\r\\n' % command);
    # 执行结果保存至文件
    Outres = tn.read_all()
    return Outres

def collectCpuinfo(OutresCpuInfo):
    # OutresCpuInfo = str(OutresCpuInfo, encoding="utf-8")

    # OutresCpuInfo = OutresCpuInfo.split(' \\r\\n')
    CpuInfo_list = str(OutresCpuInfo)
    CPU_list = CpuInfo_list.split()
    # OutresCpuInfo = OutresCpuInfo[3:5][1].split()
    # userCpuValue = float(CPU_list[9])
    userCpuValue = pfloat(CPU_list[9])
    sysCpuValue = pfloat(CPU_list[11])
    idleCpuValue = pfloat(CPU_list[15])
    ioValue = pfloat(CPU_list[17])
    # sysCpuValue = float(OutresCpuInfo[4])
    # delCpuValue = float(OutresCpuInfo[10])
    # return userCpuValue
    return (userCpuValue,sysCpuValue,idleCpuValue,ioValue)

def collectMemFree(OutresMemFree):

    OutresMemFree = OutresMemFree.decode('utf-8')
    lines = OutresMemFree.splitlines()
    lines = [line.split(":") for line in lines if ":" in line]
    lines = [(k, int(v.strip().split(' ')[0])) for [k,v] in lines]
    data = dict(lines)
    return data["MemFree"], data["MemTotal"], data["Buffers"], data["Cached"]

def GetBoxMain_pid(Boxmain):
    BoxmianPid_List = str(Boxmain).split()
    BoxmianPid = BoxmianPid_List[5]

    return BoxmianPid


def collectVMRss(OutresVmRSS):
    OutresVmRSS = str(OutresVmRSS)
    OutresVmRSS = OutresVmRSS.split('\\r\\n')
    OutresVmRSS = OutresVmRSS[1:len(OutresVmRSS)-1]
    OutresVmRSS = dict(map(lambda x: x.split(':'), OutresVmRSS))
    VmRSSValue = int(OutresVmRSS['VmRSS'].split()[0])
    return VmRSSValue

def collectNNIE(OutresNNIE):
    OutresNNIE = str(OutresNNIE)
    OutresNNIE = OutresNNIE.split('\\r\\n')

    CoreId0_CntPerSec = int(OutresNNIE[2].split()[2])
    CoreId0_MaxCntPerSec= int(OutresNNIE[2].split()[3])
    CoreId1_CntPerSec =  int(OutresNNIE[3].split()[2])
    CoreId1_MaxCntPerSec = int(OutresNNIE[3].split()[3])
    # print(CoreId0_CntPerSec,CoreId0_MaxCntPerSec,CoreId1_CntPerSec,CoreId1_MaxCntPerSec)
    return(CoreId0_CntPerSec,CoreId0_MaxCntPerSec,CoreId1_CntPerSec,CoreId1_MaxCntPerSec)

    # return (userCpuValue,sysCpuValue,idleCpuValue,ioValue)


def collectDataCenter_Rtsp_server_0(DataCenter_Rtsp_server0):
    Rtsp_server0_list = str(DataCenter_Rtsp_server0).split('\\r\\n')
    rtsp_server_0_fifo_addr = str(Rtsp_server0_list[1].split()[0])
    rtsp_server_0_cur_num = int(Rtsp_server0_list[1].split()[2])
    rtsp_server_0_max_cur_num = int(Rtsp_server0_list[1].split()[3])
    rtsp_server_0_drop_num =int(Rtsp_server0_list[1].split()[5])
    # print(rtsp_server_0_fifo_addr,rtsp_server_0_cur_num,rtsp_server_0_max_cur_num,rtsp_server_0_drop_num)
    return (rtsp_server_0_fifo_addr, rtsp_server_0_cur_num, rtsp_server_0_max_cur_num, rtsp_server_0_drop_num)

def collectDataCenter_Rtsp_server_1(DataCenter_Rtsp_server1):
    Rtsp_server1_list = str(DataCenter_Rtsp_server1).split('\\r\\n')
    rtsp_server_1_fifo_addr = str(Rtsp_server1_list[1].split()[0])
    rtsp_server_1_cur_num = int(Rtsp_server1_list[1].split()[2])
    rtsp_server_1_max_cur_num = int(Rtsp_server1_list[1].split()[3])
    rtsp_server_1_drop_num =int(Rtsp_server1_list[1].split()[5])
    # print(rtsp_server_1_fifo_addr,rtsp_server_1_cur_num,rtsp_server_1_max_cur_num,rtsp_server_1_drop_num)
    return(rtsp_server_1_fifo_addr,rtsp_server_1_cur_num,rtsp_server_1_max_cur_num,rtsp_server_1_drop_num)

def collectDataCenter_Rtsp_server_2(DataCenter_Rtsp_server2):
    Rtsp_server2_list = str(DataCenter_Rtsp_server2).split('\\r\\n')
    rtsp_server_2_fifo_addr = str(Rtsp_server2_list[1].split()[0])
    rtsp_server_2_cur_num = int(Rtsp_server2_list[1].split()[2])
    rtsp_server_2_max_cur_num = int(Rtsp_server2_list[1].split()[3])
    rtsp_server_2_drop_num =int(Rtsp_server2_list[1].split()[5])
    # print(rtsp_server_2_fifo_addr,rtsp_server_2_cur_num,rtsp_server_2_max_cur_num,rtsp_server_2_drop_num)
    return(rtsp_server_2_fifo_addr,rtsp_server_2_cur_num,rtsp_server_2_max_cur_num,rtsp_server_2_drop_num)

def collectDataCenter_Rtsp_server_3(DataCenter_Rtsp_server3):
    Rtsp_server3_list = str(DataCenter_Rtsp_server3).split('\\r\\n')
    rtsp_server_3_fifo_addr = str(Rtsp_server3_list[1].split()[0])
    rtsp_server_3_cur_num = int(Rtsp_server3_list[1].split()[2])
    rtsp_server_3_max_cur_num = int(Rtsp_server3_list[1].split()[3])
    rtsp_server_3_drop_num =int(Rtsp_server3_list[1].split()[5])
    # print(rtsp_server_3_fifo_addr,rtsp_server_3_cur_num,rtsp_server_3_max_cur_num,rtsp_server_3_drop_num)
    return(rtsp_server_3_fifo_addr,rtsp_server_3_cur_num,rtsp_server_3_max_cur_num,rtsp_server_3_drop_num)

def collectDataCenter_Rtsp_server_4(DataCenter_Rtsp_server4):
    Rtsp_server4_list = str(DataCenter_Rtsp_server4).split('\\r\\n')
    rtsp_server_4_fifo_addr = str(Rtsp_server4_list[1].split()[0])
    rtsp_server_4_cur_num = int(Rtsp_server4_list[1].split()[2])
    rtsp_server_4_max_cur_num = int(Rtsp_server4_list[1].split()[3])
    rtsp_server_4_drop_num =int(Rtsp_server4_list[1].split()[5])
    # print(rtsp_server_4_fifo_addr,rtsp_server_4_cur_num,rtsp_server_4_max_cur_num,rtsp_server_4_drop_num)
    return(rtsp_server_4_fifo_addr,rtsp_server_4_cur_num,rtsp_server_4_max_cur_num,rtsp_server_4_drop_num)

def collectDataCenter_Rtsp_server_5(DataCenter_Rtsp_server5):
    Rtsp_server5_list = str(DataCenter_Rtsp_server5).split('\\r\\n')
    rtsp_server_5_fifo_addr = str(Rtsp_server5_list[1].split()[0])
    rtsp_server_5_cur_num = int(Rtsp_server5_list[1].split()[2])
    rtsp_server_5_max_cur_num = int(Rtsp_server5_list[1].split()[3])
    rtsp_server_5_drop_num =int(Rtsp_server5_list[1].split()[5])
    # print(rtsp_server_5_fifo_addr,rtsp_server_5_cur_num,rtsp_server_5_max_cur_num,rtsp_server_5_drop_num)
    return(rtsp_server_5_fifo_addr,rtsp_server_5_cur_num,rtsp_server_5_max_cur_num,rtsp_server_5_drop_num)

def collectDataCenter_Rtsp_server_6(DataCenter_Rtsp_server6):
    Rtsp_server6_list = str(DataCenter_Rtsp_server6).split('\\r\\n')
    rtsp_server_6_fifo_addr = str(Rtsp_server6_list[1].split()[0])
    rtsp_server_6_cur_num = int(Rtsp_server6_list[1].split()[2])
    rtsp_server_6_max_cur_num = int(Rtsp_server6_list[1].split()[3])
    rtsp_server_6_drop_num =int(Rtsp_server6_list[1].split()[5])
    # print(rtsp_server_6_fifo_addr,rtsp_server_6_cur_num,rtsp_server_6_max_cur_num,rtsp_server_6_drop_num)
    return(rtsp_server_6_fifo_addr,rtsp_server_6_cur_num,rtsp_server_6_max_cur_num,rtsp_server_6_drop_num)


def collectDataCenter_Rtsp_server_7(DataCenter_Rtsp_server7):
    Rtsp_server7_list = str(DataCenter_Rtsp_server7).split('\\r\\n')
    rtsp_server_7_fifo_addr = str(Rtsp_server7_list[1].split()[0])
    rtsp_server_7_cur_num = int(Rtsp_server7_list[1].split()[2])
    rtsp_server_7_max_cur_num = int(Rtsp_server7_list[1].split()[3])
    rtsp_server_7_drop_num =int(Rtsp_server7_list[1].split()[5])
    # print(rtsp_server_7_fifo_addr,rtsp_server_7_cur_num,rtsp_server_7_max_cur_num,rtsp_server_7_drop_num)
    return(rtsp_server_7_fifo_addr,rtsp_server_7_cur_num,rtsp_server_7_max_cur_num,rtsp_server_7_drop_num)

def collectDataCenter_Rtsp_server_8(DataCenter_Rtsp_server8):
    Rtsp_server8_list = str(DataCenter_Rtsp_server8).split('\\r\\n')
    rtsp_server_8_fifo_addr = str(Rtsp_server8_list[1].split()[0])
    rtsp_server_8_cur_num = int(Rtsp_server8_list[1].split()[2])
    rtsp_server_8_max_cur_num = int(Rtsp_server8_list[1].split()[3])
    rtsp_server_8_drop_num =int(Rtsp_server8_list[1].split()[5])
    # print(rtsp_server_8_fifo_addr,rtsp_server_8_cur_num,rtsp_server_8_max_cur_num,rtsp_server_8_drop_num)
    return (rtsp_server_8_fifo_addr,rtsp_server_8_cur_num,rtsp_server_8_max_cur_num,rtsp_server_8_drop_num)

def collectDataCenter_Rtsp_server_9(DataCenter_Rtsp_server9):
    Rtsp_server9_list = str(DataCenter_Rtsp_server9).split('\\r\\n')
    rtsp_server_9_fifo_addr = str(Rtsp_server9_list[1].split()[0])
    rtsp_server_9_cur_num = int(Rtsp_server9_list[1].split()[2])
    rtsp_server_9_max_cur_num = int(Rtsp_server9_list[1].split()[3])
    rtsp_server_9_drop_num =int(Rtsp_server9_list[1].split()[5])
    # print(rtsp_server_9_fifo_addr,rtsp_server_9_cur_num,rtsp_server_9_max_cur_num,rtsp_server_9_drop_num)
    return(rtsp_server_9_fifo_addr,rtsp_server_9_cur_num,rtsp_server_9_max_cur_num,rtsp_server_9_drop_num)

def collectDataCenter_Rtsp_server_10(DataCenter_Rtsp_server10):
    Rtsp_server10_list = str(DataCenter_Rtsp_server10).split('\\r\\n')
    rtsp_server_10_fifo_addr = str(Rtsp_server10_list[1].split()[0])
    rtsp_server_10_cur_num = int(Rtsp_server10_list[1].split()[2])
    rtsp_server_10_max_cur_num = int(Rtsp_server10_list[1].split()[3])
    rtsp_server_10_drop_num =int(Rtsp_server10_list[1].split()[5])
    # print(rtsp_server_10_fifo_addr,rtsp_server_10_cur_num,rtsp_server_10_max_cur_num,rtsp_server_10_drop_num)
    return(rtsp_server_10_fifo_addr,rtsp_server_10_cur_num,rtsp_server_10_max_cur_num,rtsp_server_10_drop_num)

def collectDataCenter_Rtsp_server_11(DataCenter_Rtsp_server11):
    Rtsp_server11_list = str(DataCenter_Rtsp_server11).split('\\r\\n')
    rtsp_server_11_fifo_addr = str(Rtsp_server11_list[1].split()[0])
    rtsp_server_11_cur_num = int(Rtsp_server11_list[1].split()[2])
    rtsp_server_11_max_cur_num = int(Rtsp_server11_list[1].split()[3])
    rtsp_server_11_drop_num =int(Rtsp_server11_list[1].split()[5])
    # print(rtsp_server_11_fifo_addr,rtsp_server_11_cur_num,rtsp_server_11_max_cur_num,rtsp_server_11_drop_num)
    return(rtsp_server_11_fifo_addr,rtsp_server_11_cur_num,rtsp_server_11_max_cur_num,rtsp_server_11_drop_num)

def collectDataCenter_Rtsp_server_12(DataCenter_Rtsp_server12):
    Rtsp_server12_list = str(DataCenter_Rtsp_server12).split('\\r\\n')
    rtsp_server_12_fifo_addr = str(Rtsp_server12_list[1].split()[0])
    rtsp_server_12_cur_num = int(Rtsp_server12_list[1].split()[2])
    rtsp_server_12_max_cur_num = int(Rtsp_server12_list[1].split()[3])
    rtsp_server_12_drop_num =int(Rtsp_server12_list[1].split()[5])
    # print(rtsp_server_12_fifo_addr,rtsp_server_12_cur_num,rtsp_server_12_max_cur_num,rtsp_server_12_drop_num)
    return(rtsp_server_12_fifo_addr,rtsp_server_12_cur_num,rtsp_server_12_max_cur_num,rtsp_server_12_drop_num)

def collectDataCenter_Rtsp_server_13(DataCenter_Rtsp_server13):
    Rtsp_server13_list = str(DataCenter_Rtsp_server13).split('\\r\\n')
    rtsp_server_13_fifo_addr = str(Rtsp_server13_list[1].split()[0])
    rtsp_server_13_cur_num = int(Rtsp_server13_list[1].split()[2])
    rtsp_server_13_max_cur_num = int(Rtsp_server13_list[1].split()[3])
    rtsp_server_13_drop_num =int(Rtsp_server13_list[1].split()[5])
    # print(rtsp_server_13_fifo_addr,rtsp_server_13_cur_num,rtsp_server_13_max_cur_num,rtsp_server_13_drop_num)
    return(rtsp_server_13_fifo_addr, rtsp_server_13_cur_num, rtsp_server_13_max_cur_num, rtsp_server_13_drop_num)


def collectDataCenter_Rtsp_server_14(DataCenter_Rtsp_server14):
    Rtsp_server14_list = str(DataCenter_Rtsp_server14).split('\\r\\n')
    rtsp_server_14_fifo_addr = str(Rtsp_server14_list[1].split()[0])
    rtsp_server_14_cur_num = int(Rtsp_server14_list[1].split()[2])
    rtsp_server_14_max_cur_num = int(Rtsp_server14_list[1].split()[3])
    rtsp_server_14_drop_num =int(Rtsp_server14_list[1].split()[5])
    # print(rtsp_server_14_fifo_addr,rtsp_server_14_cur_num,rtsp_server_14_max_cur_num,rtsp_server_14_drop_num)
    return(rtsp_server_14_fifo_addr,rtsp_server_14_cur_num,rtsp_server_14_max_cur_num,rtsp_server_14_drop_num)

def collectDataCenter_Rtsp_server_15(DataCenter_Rtsp_server15):
    Rtsp_server15_list = str(DataCenter_Rtsp_server15).split('\\r\\n')
    rtsp_server_15_fifo_addr = str(Rtsp_server15_list[1].split()[0])
    rtsp_server_15_cur_num = int(Rtsp_server15_list[1].split()[2])
    rtsp_server_15_max_cur_num = int(Rtsp_server15_list[1].split()[3])
    rtsp_server_15_drop_num =int(Rtsp_server15_list[1].split()[5])
    # print(rtsp_server_15_fifo_addr,rtsp_server_15_cur_num,rtsp_server_15_max_cur_num,rtsp_server_15_drop_num)
    return(rtsp_server_15_fifo_addr,rtsp_server_15_cur_num,rtsp_server_15_max_cur_num,rtsp_server_15_drop_num)

#-------------------------------------------------------------------------------------------
def collectDataCenter_Rtsp_client_0(DataCenter_Rtsp_client0):
    Rtsp_client_0_list = str(DataCenter_Rtsp_client0).split('\\r\\n')
    rtsp_client_0_fifo_addr = str(Rtsp_client_0_list[2].split()[0])
    rtsp_client_0_cur_num = int(Rtsp_client_0_list[2].split()[2])
    rtsp_client_0_max_cur_num = int(Rtsp_client_0_list[2].split()[3])
    rtsp_client_0_drop_num =int(Rtsp_client_0_list[2].split()[5])
    # print(rtsp_client_0_fifo_addr,rtsp_client_0_cur_num,rtsp_client_0_max_cur_num,rtsp_client_0_drop_num)
    return(rtsp_client_0_fifo_addr,rtsp_client_0_cur_num,rtsp_client_0_max_cur_num,rtsp_client_0_drop_num)

def collectDataCenter_Rtsp_client_1(DataCenter_Rtsp_client1):
    Rtsp_client_1_list = str(DataCenter_Rtsp_client1).split('\\r\\n')
    rtsp_client_1_fifo_addr = str(Rtsp_client_1_list[2].split()[0])
    rtsp_client_1_cur_num = int(Rtsp_client_1_list[2].split()[2])
    rtsp_client_1_max_cur_num = int(Rtsp_client_1_list[2].split()[3])
    rtsp_client_1_drop_num =int(Rtsp_client_1_list[2].split()[5])
    # print(rtsp_client_1_fifo_addr,rtsp_client_1_cur_num,rtsp_client_1_max_cur_num,rtsp_client_1_drop_num)
    return(rtsp_client_1_fifo_addr,rtsp_client_1_cur_num,rtsp_client_1_max_cur_num,rtsp_client_1_drop_num)

def collectDataCenter_Rtsp_client_2(DataCenter_Rtsp_client2):
    Rtsp_client_2_list = str(DataCenter_Rtsp_client2).split('\\r\\n')
    rtsp_client_2_fifo_addr = str(Rtsp_client_2_list[2].split()[0])
    rtsp_client_2_cur_num = int(Rtsp_client_2_list[2].split()[2])
    rtsp_client_2_max_cur_num = int(Rtsp_client_2_list[2].split()[3])
    rtsp_client_2_drop_num =int(Rtsp_client_2_list[2].split()[5])
    # print(rtsp_client_2_fifo_addr,rtsp_client_2_cur_num,rtsp_client_2_max_cur_num,rtsp_client_2_drop_num)
    return(rtsp_client_2_fifo_addr,rtsp_client_2_cur_num,rtsp_client_2_max_cur_num,rtsp_client_2_drop_num)

def collectDataCenter_Rtsp_client_3(DataCenter_Rtsp_client3):
    Rtsp_client_3_list = str(DataCenter_Rtsp_client3).split('\\r\\n')
    rtsp_client_3_fifo_addr = str(Rtsp_client_3_list[2].split()[0])
    rtsp_client_3_cur_num = int(Rtsp_client_3_list[2].split()[2])
    rtsp_client_3_max_cur_num = int(Rtsp_client_3_list[2].split()[3])
    rtsp_client_3_drop_num =int(Rtsp_client_3_list[2].split()[5])
    # print(rtsp_client_3_fifo_addr,rtsp_client_3_cur_num,rtsp_client_3_max_cur_num,rtsp_client_3_drop_num)
    return(rtsp_client_3_fifo_addr,rtsp_client_3_cur_num,rtsp_client_3_max_cur_num,rtsp_client_3_drop_num)

def collectDataCenter_Rtsp_client_4(DataCenter_Rtsp_client4):
    Rtsp_client_4_list = str(DataCenter_Rtsp_client4).split('\\r\\n')
    rtsp_client_4_fifo_addr = str(Rtsp_client_4_list[2].split()[0])
    rtsp_client_4_cur_num = int(Rtsp_client_4_list[2].split()[2])
    rtsp_client_4_max_cur_num = int(Rtsp_client_4_list[2].split()[3])
    rtsp_client_4_drop_num =int(Rtsp_client_4_list[2].split()[5])
    # print(rtsp_client_4_fifo_addr,rtsp_client_4_cur_num,rtsp_client_4_max_cur_num,rtsp_client_4_drop_num)
    return(rtsp_client_4_fifo_addr,rtsp_client_4_cur_num,rtsp_client_4_max_cur_num,rtsp_client_4_drop_num)

def collectDataCenter_Rtsp_client_5(DataCenter_Rtsp_client5):
    Rtsp_client_5_list = str(DataCenter_Rtsp_client5).split('\\r\\n')
    rtsp_client_5_fifo_addr = str(Rtsp_client_5_list[2].split()[0])
    rtsp_client_5_cur_num = int(Rtsp_client_5_list[2].split()[2])
    rtsp_client_5_max_cur_num = int(Rtsp_client_5_list[2].split()[3])
    rtsp_client_5_drop_num =int(Rtsp_client_5_list[2].split()[5])
    # print(rtsp_client_5_fifo_addr,rtsp_client_5_cur_num,rtsp_client_5_max_cur_num,rtsp_client_5_drop_num)
    return(rtsp_client_5_fifo_addr,rtsp_client_5_cur_num,rtsp_client_5_max_cur_num,rtsp_client_5_drop_num)

def collectDataCenter_Rtsp_client_6(DataCenter_Rtsp_client6):
    Rtsp_client_6_list = str(DataCenter_Rtsp_client6).split('\\r\\n')
    rtsp_client_6_fifo_addr = str(Rtsp_client_6_list[2].split()[0])
    rtsp_client_6_cur_num = int(Rtsp_client_6_list[2].split()[2])
    rtsp_client_6_max_cur_num = int(Rtsp_client_6_list[2].split()[3])
    rtsp_client_6_drop_num =int(Rtsp_client_6_list[2].split()[5])
    # print(rtsp_client_6_fifo_addr,rtsp_client_6_cur_num,rtsp_client_6_max_cur_num,rtsp_client_6_drop_num)
    return(rtsp_client_6_fifo_addr,rtsp_client_6_cur_num,rtsp_client_6_max_cur_num,rtsp_client_6_drop_num)

def collectDataCenter_Rtsp_client_7(DataCenter_Rtsp_client7):
    Rtsp_client_7_list = str(DataCenter_Rtsp_client7).split('\\r\\n')
    rtsp_client_7_fifo_addr = str(Rtsp_client_7_list[2].split()[0])
    rtsp_client_7_cur_num = int(Rtsp_client_7_list[2].split()[2])
    rtsp_client_7_max_cur_num = int(Rtsp_client_7_list[2].split()[3])
    rtsp_client_7_drop_num =int(Rtsp_client_7_list[2].split()[5])
    # print(rtsp_client_7_fifo_addr,rtsp_client_7_cur_num,rtsp_client_7_max_cur_num,rtsp_client_7_drop_num)
    return(rtsp_client_7_fifo_addr,rtsp_client_7_cur_num,rtsp_client_7_max_cur_num,rtsp_client_7_drop_num)

def collectDataCenter_Rtsp_client_8(DataCenter_Rtsp_client8):
    Rtsp_client_8_list = str(DataCenter_Rtsp_client8).split('\\r\\n')
    rtsp_client_8_fifo_addr = str(Rtsp_client_8_list[2].split()[0])
    rtsp_client_8_cur_num = int(Rtsp_client_8_list[2].split()[2])
    rtsp_client_8_max_cur_num = int(Rtsp_client_8_list[2].split()[3])
    rtsp_client_8_drop_num =int(Rtsp_client_8_list[2].split()[5])
    # print(rtsp_client_8_fifo_addr,rtsp_client_8_cur_num,rtsp_client_8_max_cur_num,rtsp_client_8_drop_num)
    return(rtsp_client_8_fifo_addr,rtsp_client_8_cur_num,rtsp_client_8_max_cur_num,rtsp_client_8_drop_num)

def collectDataCenter_Rtsp_client_9(DataCenter_Rtsp_client9):
    Rtsp_client_9_list = str(DataCenter_Rtsp_client9).split('\\r\\n')
    rtsp_client_9_fifo_addr = str(Rtsp_client_9_list[2].split()[0])
    rtsp_client_9_cur_num = int(Rtsp_client_9_list[2].split()[2])
    rtsp_client_9_max_cur_num = int(Rtsp_client_9_list[2].split()[3])
    rtsp_client_9_drop_num =int(Rtsp_client_9_list[2].split()[5])
    # print(rtsp_client_9_fifo_addr,rtsp_client_9_cur_num,rtsp_client_9_max_cur_num,rtsp_client_9_drop_num)
    return(rtsp_client_9_fifo_addr, rtsp_client_9_cur_num, rtsp_client_9_max_cur_num, rtsp_client_9_drop_num)

def collectDataCenter_Rtsp_client_10(DataCenter_Rtsp_client10):
    Rtsp_client_10_list = str(DataCenter_Rtsp_client10).split('\\r\\n')
    rtsp_client_10_fifo_addr = str(Rtsp_client_10_list[2].split()[0])
    rtsp_client_10_cur_num = int(Rtsp_client_10_list[2].split()[2])
    rtsp_client_10_max_cur_num = int(Rtsp_client_10_list[2].split()[3])
    rtsp_client_10_drop_num =int(Rtsp_client_10_list[2].split()[5])
    # print(rtsp_client_10_fifo_addr,rtsp_client_10_cur_num,rtsp_client_10_max_cur_num,rtsp_client_10_drop_num)
    return(rtsp_client_10_fifo_addr,rtsp_client_10_cur_num,rtsp_client_10_max_cur_num,rtsp_client_10_drop_num)

def collectDataCenter_Rtsp_client_11(DataCenter_Rtsp_client11):
    Rtsp_client_11_list = str(DataCenter_Rtsp_client11).split('\\r\\n')
    rtsp_client_11_fifo_addr = str(Rtsp_client_11_list[2].split()[0])
    rtsp_client_11_cur_num = int(Rtsp_client_11_list[2].split()[2])
    rtsp_client_11_max_cur_num = int(Rtsp_client_11_list[2].split()[3])
    rtsp_client_11_drop_num =int(Rtsp_client_11_list[2].split()[5])
    # print(rtsp_client_11_fifo_addr,rtsp_client_11_cur_num,rtsp_client_11_max_cur_num,rtsp_client_11_drop_num)
    return(rtsp_client_11_fifo_addr, rtsp_client_11_cur_num, rtsp_client_11_max_cur_num, rtsp_client_11_drop_num)

def collectDataCenter_Rtsp_client_12(DataCenter_Rtsp_client12):
    Rtsp_client_12_list = str(DataCenter_Rtsp_client12).split('\\r\\n')
    rtsp_client_12_fifo_addr = str(Rtsp_client_12_list[2].split()[0])
    rtsp_client_12_cur_num = int(Rtsp_client_12_list[2].split()[2])
    rtsp_client_12_max_cur_num = int(Rtsp_client_12_list[2].split()[3])
    rtsp_client_12_drop_num =int(Rtsp_client_12_list[2].split()[5])
    # print(rtsp_client_12_fifo_addr,rtsp_client_12_cur_num,rtsp_client_12_max_cur_num,rtsp_client_12_drop_num)
    return(rtsp_client_12_fifo_addr,rtsp_client_12_cur_num,rtsp_client_12_max_cur_num,rtsp_client_12_drop_num)

def collectDataCenter_Rtsp_client_13(DataCenter_Rtsp_client13):
    Rtsp_client_13_list = str(DataCenter_Rtsp_client13).split('\\r\\n')
    rtsp_client_13_fifo_addr = str(Rtsp_client_13_list[2].split()[0])
    rtsp_client_13_cur_num = int(Rtsp_client_13_list[2].split()[2])
    rtsp_client_13_max_cur_num = int(Rtsp_client_13_list[2].split()[3])
    rtsp_client_13_drop_num =int(Rtsp_client_13_list[2].split()[5])
    # print(rtsp_client_13_fifo_addr,rtsp_client_13_cur_num,rtsp_client_13_max_cur_num,rtsp_client_13_drop_num)
    return(rtsp_client_13_fifo_addr, rtsp_client_13_cur_num, rtsp_client_13_max_cur_num, rtsp_client_13_drop_num)

def collectDataCenter_Rtsp_client_14(DataCenter_Rtsp_client14):
    Rtsp_client_14_list = str(DataCenter_Rtsp_client14).split('\\r\\n')
    rtsp_client_14_fifo_addr = str(Rtsp_client_14_list[2].split()[0])
    rtsp_client_14_cur_num = int(Rtsp_client_14_list[2].split()[2])
    rtsp_client_14_max_cur_num = int(Rtsp_client_14_list[2].split()[3])
    rtsp_client_14_drop_num =int(Rtsp_client_14_list[2].split()[5])
    # print(rtsp_client_14_fifo_addr,rtsp_client_14_cur_num,rtsp_client_14_max_cur_num,rtsp_client_14_drop_num)
    return(rtsp_client_14_fifo_addr, rtsp_client_14_cur_num, rtsp_client_14_max_cur_num, rtsp_client_14_drop_num)

def collectDataCenter_Rtsp_client_15(DataCenter_Rtsp_client15):
    Rtsp_client_15_list = str(DataCenter_Rtsp_client15).split('\\r\\n')
    rtsp_client_15_fifo_addr = str(Rtsp_client_15_list[2].split()[0])
    rtsp_client_15_cur_num = int(Rtsp_client_15_list[2].split()[2])
    rtsp_client_15_max_cur_num = int(Rtsp_client_15_list[2].split()[3])
    rtsp_client_15_drop_num =int(Rtsp_client_15_list[2].split()[5])
    # print(rtsp_client_15_fifo_addr,rtsp_client_15_cur_num,rtsp_client_15_max_cur_num,rtsp_client_15_drop_num)
    return(rtsp_client_15_fifo_addr,rtsp_client_15_cur_num,rtsp_client_15_max_cur_num,rtsp_client_15_drop_num)

def collectDataCenter_rtsp_server_setsei(DataCenter_rtsp_server_setsei):
    rtsp_server_setsei_list = str(DataCenter_rtsp_server_setsei).split('\\r\\n')
    cur_numValue = int(rtsp_server_setsei_list[1].split()[2])
    max_numValue = int(rtsp_server_setsei_list[1].split()[3])
    max_cur_numValue = int(rtsp_server_setsei_list[1].split()[4])
    pkg_mem_sizeValue = int(rtsp_server_setsei_list[1].split()[5])

    return (cur_numValue,max_numValue,max_cur_numValue,pkg_mem_sizeValue)

def collectDataCenter_web_server(DataCenter_web_server):
    DataCenter_web_server_list = str(DataCenter_web_server).split('\\r\\n')
    cur_numValue = int(DataCenter_web_server_list[1].split()[2])
    max_numValue = int(DataCenter_web_server_list[1].split()[3])
    max_cur_numValue = int(DataCenter_web_server_list[1].split()[4])
    pkg_mem_sizeValue = int(DataCenter_web_server_list[1].split()[5])

    return (cur_numValue,max_numValue,max_cur_numValue,pkg_mem_sizeValue)

def collectuptime(uptime):
    collectuptime = str(uptime).split('\\r\\n')
    collectuptime = collectuptime[1].split()[2]+","+collectuptime[1].split()[3]
    uptime = collectuptime
    if "min" in uptime:
        # print(uptime.split(',')[0])
        uptime = int(uptime.split(',')[0])
        return uptime
    elif ":" in uptime:
        uptime = uptime.split(',')[0]
        h,m = uptime.split(':')
        # print(int(h)*60+int(m))
        uptime = int(int(h)*60+int(m))
        return uptime
    elif "days" in uptime:
         uptime = int(uptime.split(',')[0])
         uptime = int(uptime*24*60)
         print(uptime)
         return uptime
    else:
        print("not match!")


#-------------------连接InfluxDB------------------------------
def CPU_DataToInfluxDB(Host,userCpu,sysCpu,idleCpu,ioCpu):
    #now = datetime.datetime.now()
    #t = datetime.datetime.fromtimestamp(now.timestamp()).isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
    data_list = [{
        'measurement': 'CPU',
        'tags': {'deviceIP': Host},
        'fields': {
            'userCpu': userCpu,
            'sysCpu': sysCpu,
            'idelCpu': idleCpu,
            'ioCpu' :ioCpu
        },
    }]
    return data_list

def uptime_DataToInfluxDB(Host,uptime):
    #now = datetime.datetime.now()
    #t = datetime.datetime.fromtimestamp(now.timestamp()).isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
    data_list = [{
        'measurement': 'uptime',
        'tags': {'deviceIP': Host},
        'fields': {
            'uptime': uptime,
        },
    }]
    return data_list
# def Mem_DataToInfluxDB(Host,MemFree,Vmrss):
# def Mem_DataToInfluxDB(Host,MemFree,Vmrss):
#     #now = datetime.datetime.now()
#     #t = datetime.datetime.fromtimestamp(now.timestamp()).isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
#     data_list = [{
#         'measurement': 'Memory',
#         'tags': {'deviceIP': Host},
#         'fields': {
#             'sysMemFree': MemFree,
#             'ProVmrss': Vmrss
#         },
#     }]
#     return data_list

def Mem_DataToInfluxDB(Host,MemFree,MemTotal,Buffers,Cached,Vmrss):
    data_list = [{
        'measurement': 'Memory',
        'tags': {'deviceIP': Host},
        'fields': {
            'MemFree': MemFree,
            'MemTotal' : MemTotal,
            'Buffers': Buffers,
            'Cached' : Cached,
            'ProVmrss': Vmrss
        },
    }]
    return data_list

def NNIE_DataToInfluxDB(Host,CoreId0_CntPerSec,CoreId0_MaxCntPerSec,CoreId1_CntPerSec,CoreId1_MaxCntPerSec):
    data_list = [{
        'measurement': 'NNIE',
        'tags': {'deviceIP': Host},
        'fields': {
            'CoreId0_CntPerSec': CoreId0_CntPerSec,
            'CoreId0_MaxCntPerSec': CoreId0_MaxCntPerSec,
            'CoreId1_CntPerSec': CoreId1_CntPerSec,
            'CoreId1_MaxCntPerSec': CoreId1_MaxCntPerSec
        },
    }]
    return data_list

def DataCenter_DataToInfluxDB(Host,cur_num2,max_num2,max_cur_num2,pkg_mem_size2,cur_num3,max_num3,max_cur_num3,pkg_mem_size3):
    data_list = [{
        'measurement': 'DataCenter',
        'tags': {'deviceIP': Host},
        'fields': {
            'Rtspserversetsei_cur_num':cur_num2,
            'Rtspserversetsei_max_num': max_num2,
            'Rtspserversetsei_max_cur_num':max_cur_num2,
            'Rtspserversetsei_pkg_mem_size_size':pkg_mem_size2,
            'WebServe_cur_num': cur_num3,
            'WebServe_cur_num_max_num': max_num3,
            'WebServe_cur_num_max_cur_num': max_cur_num3,
            'WebServe_cur_num_pkg_mem_size': pkg_mem_size3,
        },
    }]
    return data_list

def Rtsp_server_fifo_addr_DataToInfluxDB(Host,rtsp_server_0_fifo_addr,rtsp_server_1_fifo_addr,rtsp_server_2_fifo_addr,rtsp_server_3_fifo_addr,rtsp_server_4_fifo_addr,rtsp_server_5_fifo_addr,rtsp_server_6_fifo_addr,rtsp_server_7_fifo_addr,rtsp_server_8_fifo_addr,rtsp_server_9_fifo_addr,rtsp_server_10_fifo_addr,rtsp_server_11_fifo_addr,rtsp_server_12_fifo_addr,rtsp_server_13_fifo_addr,rtsp_server_14_fifo_addr,rtsp_server_15_fifo_addr):
    data_list = [{
        'measurement': 'DataCenterRtsp_server_fifo_addr',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_server_0_fifo_addr': rtsp_server_0_fifo_addr,
            'rtsp_server_1_fifo_addr': rtsp_server_1_fifo_addr,
            'rtsp_server_2_fifo_addr': rtsp_server_2_fifo_addr,
            'rtsp_server_3_fifo_addr': rtsp_server_3_fifo_addr,
            'rtsp_server_4_fifo_addr': rtsp_server_4_fifo_addr,
            'rtsp_server_5_fifo_addr': rtsp_server_5_fifo_addr,
            'rtsp_server_6_fifo_addr': rtsp_server_6_fifo_addr,
            'rtsp_server_7_fifo_addr': rtsp_server_7_fifo_addr,
            'rtsp_server_8_fifo_addr': rtsp_server_8_fifo_addr,
            'rtsp_server_9_fifo_addr': rtsp_server_9_fifo_addr,
            'rtsp_server_10_fifo_addr': rtsp_server_10_fifo_addr,
            'rtsp_server_11_fifo_addr': rtsp_server_11_fifo_addr,
            'rtsp_server_12_fifo_addr': rtsp_server_12_fifo_addr,
            'rtsp_server_13_fifo_addr': rtsp_server_13_fifo_addr,
            'rtsp_server_14_fifo_addr': rtsp_server_14_fifo_addr,
            'rtsp_server_15_fifo_addr': rtsp_server_15_fifo_addr,

        },
    }]
    return data_list

def Rtsp_server_cur_num_DataToInfluxDB(Host,rtsp_server_0_cur_num,rtsp_server_1_cur_num,rtsp_server_2_cur_num,rtsp_server_3_cur_num,rtsp_server_4_cur_num,rtsp_server_5_cur_num,rtsp_server_6_cur_num,rtsp_server_7_cur_num,rtsp_server_8_cur_num,rtsp_server_9_cur_num,rtsp_server_10_cur_num,rtsp_server_11_cur_num,rtsp_server_12_cur_num,rtsp_server_13_cur_num,rtsp_server_14_cur_num,rtsp_server_15_cur_num):
    data_list = [{
        'measurement': 'DataCenterRtsp_server_cur_num',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_server_0_cur_num': rtsp_server_0_cur_num,
            'rtsp_server_1_cur_num': rtsp_server_1_cur_num,
            'rtsp_server_2_cur_num': rtsp_server_2_cur_num,
            'rtsp_server_3_cur_num': rtsp_server_3_cur_num,
            'rtsp_server_4_cur_num': rtsp_server_4_cur_num,
            'rtsp_server_5_cur_num': rtsp_server_5_cur_num,
            'rtsp_server_6_cur_num': rtsp_server_6_cur_num,
            'rtsp_server_7_cur_num': rtsp_server_7_cur_num,
            'rtsp_server_8_cur_num': rtsp_server_8_cur_num,
            'rtsp_server_9_cur_num': rtsp_server_9_cur_num,
            'rtsp_server_10_cur_num': rtsp_server_10_cur_num,
            'rtsp_server_11_cur_num': rtsp_server_11_cur_num,
            'rtsp_server_12_cur_num': rtsp_server_12_cur_num,
            'rtsp_server_13_cur_num': rtsp_server_13_cur_num,
            'rtsp_server_14_cur_num': rtsp_server_14_cur_num,
            'rtsp_server_15_cur_num': rtsp_server_15_cur_num,

        },
    }]
    return data_list

# def Rtsp_server_max_num_DataToInfluxDB(Host,rtsp_server_0_max_num,rtsp_server_1_max_num,rtsp_server_2_max_num,rtsp_server_3_max_num,rtsp_server_4_max_num,rtsp_server_5_max_num,rtsp_server_6_max_num,rtsp_server_7_max_num,rtsp_server_8_max_num,rtsp_server_9_max_num,rtsp_server_10_max_num,rtsp_server_11_max_num,rtsp_server_12_max_num,rtsp_server_13_max_num,rtsp_server_14_max_num,rtsp_server_15_max_num):
#     data_list = [{
#         'measurement': 'DataCenterRtsp_server_max_num',
#         'tags': {'deviceIP': Host},
#         'fields': {
#             'rtsp_server_0_max_num': rtsp_server_0_max_num,
#             'rtsp_server_1_max_num': rtsp_server_1_max_num,
#             'rtsp_server_2_max_num': rtsp_server_2_max_num,
#             'rtsp_server_3_max_num': rtsp_server_3_max_num,
#             'rtsp_server_4_max_num': rtsp_server_4_max_num,
#             'rtsp_server_5_max_num': rtsp_server_5_max_num,
#             'rtsp_server_6_max_num': rtsp_server_6_max_num,
#             'rtsp_server_7_max_num': rtsp_server_7_max_num,
#             'rtsp_server_8_max_num': rtsp_server_8_max_num,
#             'rtsp_server_9_max_num': rtsp_server_9_max_num,
#             'rtsp_server_10_max_num': rtsp_server_10_max_num,
#             'rtsp_server_11_max_num': rtsp_server_11_max_num,
#             'rtsp_server_12_max_num': rtsp_server_12_max_num,
#             'rtsp_server_13_max_num': rtsp_server_13_max_num,
#             'rtsp_server_14_max_num': rtsp_server_14_max_num,
#             'rtsp_server_15_max_num': rtsp_server_15_max_num,
#
#         },
#     }]
#     return data_list
def Rtsp_server_max_cur_num_DataToInfluxDB(Host,rtsp_server_0_max_cur_num,rtsp_server_1_max_cur_num,rtsp_server_2_max_cur_num,rtsp_server_3_max_cur_num,rtsp_server_4_max_cur_num,rtsp_server_5_max_cur_num,rtsp_server_6_max_cur_num,rtsp_server_7_max_cur_num,rtsp_server_8_max_cur_num,rtsp_server_9_max_cur_num,rtsp_server_10_max_cur_num,rtsp_server_11_max_cur_num,rtsp_server_12_max_cur_num,rtsp_server_13_max_cur_num,rtsp_server_14_max_cur_num,rtsp_server_15_max_cur_num):
    data_list = [{
        'measurement': 'DataCenterRtsp_server_max_cur_num',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_server_0_max_cur_num': rtsp_server_0_max_cur_num,
            'rtsp_server_1_max_cur_num': rtsp_server_1_max_cur_num,
            'rtsp_server_2_max_cur_num': rtsp_server_2_max_cur_num,
            'rtsp_server_3_max_cur_num': rtsp_server_3_max_cur_num,
            'rtsp_server_4_max_cur_num': rtsp_server_4_max_cur_num,
            'rtsp_server_5_max_cur_num': rtsp_server_5_max_cur_num,
            'rtsp_server_6_max_cur_num': rtsp_server_6_max_cur_num,
            'rtsp_server_7_max_cur_num': rtsp_server_7_max_cur_num,
            'rtsp_server_8_max_cur_num': rtsp_server_8_max_cur_num,
            'rtsp_server_9_max_cur_num': rtsp_server_9_max_cur_num,
            'rtsp_server_10_max_cur_num': rtsp_server_10_max_cur_num,
            'rtsp_server_11_max_cur_num': rtsp_server_11_max_cur_num,
            'rtsp_server_12_max_cur_num': rtsp_server_12_max_cur_num,
            'rtsp_server_13_max_cur_num': rtsp_server_13_max_cur_num,
            'rtsp_server_14_max_cur_num': rtsp_server_14_max_cur_num,
            'rtsp_server_15_max_cur_num': rtsp_server_15_max_cur_num,

        },
    }]
    return data_list

def Rtsp_server_drop_num_DataToInfluxDB(Host,rtsp_server_0_drop_num,rtsp_server_1_drop_num,rtsp_server_2_drop_num,rtsp_server_3_drop_num,rtsp_server_4_drop_num,rtsp_server_5_drop_num,rtsp_server_6_drop_num,rtsp_server_7_drop_num,rtsp_server_8_drop_num,rtsp_server_9_drop_num,rtsp_server_10_drop_num,rtsp_server_11_drop_num,rtsp_server_12_drop_num,rtsp_server_13_drop_num,rtsp_server_14_drop_num,rtsp_server_15_drop_num):
    data_list = [{
        'measurement': 'DataCenterRtsp_server_drop_num',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_server_0_drop_num': rtsp_server_0_drop_num,
            'rtsp_server_1_drop_num': rtsp_server_1_drop_num,
            'rtsp_server_2_drop_num': rtsp_server_2_drop_num,
            'rtsp_server_3_drop_num': rtsp_server_3_drop_num,
            'rtsp_server_4_drop_num': rtsp_server_4_drop_num,
            'rtsp_server_5_drop_num': rtsp_server_5_drop_num,
            'rtsp_server_6_drop_num': rtsp_server_6_drop_num,
            'rtsp_server_7_drop_num': rtsp_server_7_drop_num,
            'rtsp_server_8_drop_num': rtsp_server_8_drop_num,
            'rtsp_server_9_drop_num': rtsp_server_9_drop_num,
            'rtsp_server_10_drop_num': rtsp_server_10_drop_num,
            'rtsp_server_11_drop_num': rtsp_server_11_drop_num,
            'rtsp_server_12_drop_num': rtsp_server_12_drop_num,
            'rtsp_server_13_drop_num': rtsp_server_13_drop_num,
            'rtsp_server_14_drop_num': rtsp_server_14_drop_num,
            'rtsp_server_15_drop_num': rtsp_server_15_drop_num,

        },
    }]
    return data_list

def Rtsp_client_fifo_addr_DataToInfluxDB(Host,rtsp_client_0_fifo_addr,rtsp_client_1_fifo_addr,rtsp_client_2_fifo_addr,rtsp_client_3_fifo_addr,rtsp_client_4_fifo_addr,rtsp_client_5_fifo_addr,rtsp_client_6_fifo_addr,rtsp_client_7_fifo_addr,rtsp_client_8_fifo_addr,rtsp_client_9_fifo_addr,rtsp_client_10_fifo_addr,rtsp_client_11_fifo_addr,rtsp_client_12_fifo_addr,rtsp_client_13_fifo_addr,rtsp_client_14_fifo_addr,rtsp_client_15_fifo_addr):
    data_list = [{
        'measurement': 'DataCenterRtsp_client_fifo_addr',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_client_0_fifo_addr': rtsp_client_0_fifo_addr,
            'rtsp_client_1_fifo_addr': rtsp_client_1_fifo_addr,
            'rtsp_client_2_fifo_addr': rtsp_client_2_fifo_addr,
            'rtsp_client_3_fifo_addr': rtsp_client_3_fifo_addr,
            'rtsp_client_4_fifo_addr': rtsp_client_4_fifo_addr,
            'rtsp_client_5_fifo_addr': rtsp_client_5_fifo_addr,
            'rtsp_client_6_fifo_addr': rtsp_client_6_fifo_addr,
            'rtsp_client_7_fifo_addr': rtsp_client_7_fifo_addr,
            'rtsp_client_8_fifo_addr': rtsp_client_8_fifo_addr,
            'rtsp_client_9_fifo_addr': rtsp_client_9_fifo_addr,
            'rtsp_client_10_fifo_addr': rtsp_client_10_fifo_addr,
            'rtsp_client_11_fifo_addr': rtsp_client_11_fifo_addr,
            'rtsp_client_12_fifo_addr': rtsp_client_12_fifo_addr,
            'rtsp_client_13_fifo_addr': rtsp_client_13_fifo_addr,
            'rtsp_client_14_fifo_addr': rtsp_client_14_fifo_addr,
            'rtsp_client_15_fifo_addr': rtsp_client_15_fifo_addr,

        },
    }]
    return data_list

def Rtsp_client_cur_num_DataToInfluxDB(Host,rtsp_client_0_cur_num,rtsp_client_1_cur_num,rtsp_client_2_cur_num,rtsp_client_3_cur_num,rtsp_client_4_cur_num,rtsp_client_5_cur_num,rtsp_client_6_cur_num,rtsp_client_7_cur_num,rtsp_client_8_cur_num,rtsp_client_9_cur_num,rtsp_client_10_cur_num,rtsp_client_11_cur_num,rtsp_client_12_cur_num,rtsp_client_13_cur_num,rtsp_client_14_cur_num,rtsp_client_15_cur_num):
    data_list = [{
        'measurement': 'DataCenterRtsp_client_cur_num',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_client_0_cur_num': rtsp_client_0_cur_num,
            'rtsp_client_1_cur_num': rtsp_client_1_cur_num,
            'rtsp_client_2_cur_num': rtsp_client_2_cur_num,
            'rtsp_client_3_cur_num': rtsp_client_3_cur_num,
            'rtsp_client_4_cur_num': rtsp_client_4_cur_num,
            'rtsp_client_5_cur_num': rtsp_client_5_cur_num,
            'rtsp_client_6_cur_num': rtsp_client_6_cur_num,
            'rtsp_client_7_cur_num': rtsp_client_7_cur_num,
            'rtsp_client_8_cur_num': rtsp_client_8_cur_num,
            'rtsp_client_9_cur_num': rtsp_client_9_cur_num,
            'rtsp_client_10_cur_num': rtsp_client_10_cur_num,
            'rtsp_client_11_cur_num': rtsp_client_11_cur_num,
            'rtsp_client_12_cur_num': rtsp_client_12_cur_num,
            'rtsp_client_13_cur_num': rtsp_client_13_cur_num,
            'rtsp_client_14_cur_num': rtsp_client_14_cur_num,
            'rtsp_client_15_cur_num': rtsp_client_15_cur_num,

        },
    }]
    return data_list

# def Rtsp_client_max_num_DataToInfluxDB(Host,rtsp_client_0_max_num,rtsp_client_1_max_num,rtsp_client_2_max_num,rtsp_client_3_max_num,rtsp_client_4_max_num,rtsp_client_5_max_num,rtsp_client_6_max_num,rtsp_client_7_max_num,rtsp_client_8_max_num,rtsp_client_9_max_num,rtsp_client_10_max_num,rtsp_client_11_max_num,rtsp_client_12_max_num,rtsp_client_13_max_num,rtsp_client_14_max_num,rtsp_client_15_max_num):
#     data_list = [{
#         'measurement': 'DataCenterRtsp_client_max_num',
#         'tags': {'deviceIP': Host},
#         'fields': {
#             'rtsp_client_0_max_num': rtsp_client_0_max_num,
#             'rtsp_client_1_max_num': rtsp_client_1_max_num,
#             'rtsp_client_2_max_num': rtsp_client_2_max_num,
#             'rtsp_client_3_max_num': rtsp_client_3_max_num,
#             'rtsp_client_4_max_num': rtsp_client_4_max_num,
#             'rtsp_client_5_max_num': rtsp_client_5_max_num,
#             'rtsp_client_6_max_num': rtsp_client_6_max_num,
#             'rtsp_client_7_max_num': rtsp_client_7_max_num,
#             'rtsp_client_8_max_num': rtsp_client_8_max_num,
#             'rtsp_client_9_max_num': rtsp_client_9_max_num,
#             'rtsp_client_10_max_num': rtsp_client_10_max_num,
#             'rtsp_client_11_max_num': rtsp_client_11_max_num,
#             'rtsp_client_12_max_num': rtsp_client_12_max_num,
#             'rtsp_client_13_max_num': rtsp_client_13_max_num,
#             'rtsp_client_14_max_num': rtsp_client_14_max_num,
#             'rtsp_client_15_max_num': rtsp_client_15_max_num,
#
#         },
#     }]
#     return data_list

def Rtsp_client_max_cur_num_DataToInfluxDB(Host,rtsp_client_0_max_cur_num,rtsp_client_1_max_cur_num,rtsp_client_2_max_cur_num,rtsp_client_3_max_cur_num,rtsp_client_4_max_cur_num,rtsp_client_5_max_cur_num,rtsp_client_6_max_cur_num,rtsp_client_7_max_cur_num,rtsp_client_8_max_cur_num,rtsp_client_9_max_cur_num,rtsp_client_10_max_cur_num,rtsp_client_11_max_cur_num,rtsp_client_12_max_cur_num,rtsp_client_13_max_cur_num,rtsp_client_14_max_cur_num,rtsp_client_15_max_cur_num):
    data_list = [{
        'measurement': 'DataCenterRtsp_client_max_cur_num',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_client_0_max_cur_num': rtsp_client_0_max_cur_num,
            'rtsp_client_1_max_cur_num': rtsp_client_1_max_cur_num,
            'rtsp_client_2_max_cur_num': rtsp_client_2_max_cur_num,
            'rtsp_client_3_max_cur_num': rtsp_client_3_max_cur_num,
            'rtsp_client_4_max_cur_num': rtsp_client_4_max_cur_num,
            'rtsp_client_5_max_cur_num': rtsp_client_5_max_cur_num,
            'rtsp_client_6_max_cur_num': rtsp_client_6_max_cur_num,
            'rtsp_client_7_max_cur_num': rtsp_client_7_max_cur_num,
            'rtsp_client_8_max_cur_num': rtsp_client_8_max_cur_num,
            'rtsp_client_9_max_cur_num': rtsp_client_9_max_cur_num,
            'rtsp_client_10_max_cur_num': rtsp_client_10_max_cur_num,
            'rtsp_client_11_max_cur_num': rtsp_client_11_max_cur_num,
            'rtsp_client_12_max_cur_num': rtsp_client_12_max_cur_num,
            'rtsp_client_13_max_cur_num': rtsp_client_13_max_cur_num,
            'rtsp_client_14_max_cur_num': rtsp_client_14_max_cur_num,
            'rtsp_client_15_max_cur_num': rtsp_client_15_max_cur_num,

        },
    }]
    return data_list
def Rtsp_client_drop_num_DataToInfluxDB(Host,rtsp_client_0_drop_num,rtsp_client_1_drop_num,rtsp_client_2_drop_num,rtsp_client_3_drop_num,rtsp_client_4_drop_num,rtsp_client_5_drop_num,rtsp_client_6_drop_num,rtsp_client_7_drop_num,rtsp_client_8_drop_num,rtsp_client_9_drop_num,rtsp_client_10_drop_num,rtsp_client_11_drop_num,rtsp_client_12_drop_num,rtsp_client_13_drop_num,rtsp_client_14_drop_num,rtsp_client_15_drop_num):
    data_list = [{
        'measurement': 'DataCenterRtsp_client_drop_num',
        'tags': {'deviceIP': Host},
        'fields': {
            'rtsp_client_0_drop_num': rtsp_client_0_drop_num,
            'rtsp_client_1_drop_num': rtsp_client_1_drop_num,
            'rtsp_client_2_drop_num': rtsp_client_2_drop_num,
            'rtsp_client_3_drop_num': rtsp_client_3_drop_num,
            'rtsp_client_4_drop_num': rtsp_client_4_drop_num,
            'rtsp_client_5_drop_num': rtsp_client_5_drop_num,
            'rtsp_client_6_drop_num': rtsp_client_6_drop_num,
            'rtsp_client_7_drop_num': rtsp_client_7_drop_num,
            'rtsp_client_8_drop_num': rtsp_client_8_drop_num,
            'rtsp_client_9_drop_num': rtsp_client_9_drop_num,
            'rtsp_client_10_drop_num': rtsp_client_10_drop_num,
            'rtsp_client_11_drop_num': rtsp_client_11_drop_num,
            'rtsp_client_12_drop_num': rtsp_client_12_drop_num,
            'rtsp_client_13_drop_num': rtsp_client_13_drop_num,
            'rtsp_client_14_drop_num': rtsp_client_14_drop_num,
            'rtsp_client_15_drop_num': rtsp_client_15_drop_num,

        },
    }]
    return data_list

# def DataCenter_rtsp_server_DataToInfluxDB():
#     data_list = [{
#         'measurement': 'DataCenter_rtsp_server',
#         'tags': {'deviceIP': Host},
#         'fields': {
#
#             'Rtspserversetsei_cur_num':cur_num2,
#             'Rtspserversetsei_max_num': max_num2,
#             'Rtspserversetsei_max_cur_num':max_cur_num2,
#             'Rtspserversetsei_pkg_mem_size_size':pkg_mem_size2,
#             'WebServe_cur_num': cur_num3,
#             'WebServe_cur_num_max_num': max_num3,
#             'WebServe_cur_num_max_cur_num': max_cur_num3,
#             'WebServe_cur_num_pkg_mem_size': pkg_mem_size3,
#         },
#     }]
#     return data_list

def run(Host):
    host = Host
    num =1
    maxNum =1
    while num <= maxNum:
        try:
            Boxmain = do_telnet(host, username, password, finish, BoxmainPidCommand)
            BoxmianPid_List = str(Boxmain).split()
            BoxmianPid = BoxmianPid_List[5]
            VmRSSCommand = bytes("cat /proc/%s/status;exit\n" % BoxmianPid, encoding="utf8")
            OutresCpuInfo = do_telnet(host, username, password, finish, cpuInfoCommand)
            userCpu, sysCpu, idleCpu, ioCpu = collectCpuinfo(OutresCpuInfo)

            OutresMemFree = do_telnet(host, username, password, finish, memFreeCommand)
            MemFree,MemTotal,Buffers,Cached= collectMemFree(OutresMemFree)

            OutresVmRSS = do_telnet(host, username, password, finish, VmRSSCommand)
            Vmrss = collectVMRss(OutresVmRSS)

            OutresNNIE = do_telnet(host, username, password, finish, NNIECommand)
            CoreId0_CntPerSec,CoreId0_MaxCntPerSec,CoreId1_CntPerSec,CoreId1_MaxCntPerSec = collectNNIE(OutresNNIE)

            DataCenter_Rtsp_server0 = do_telnet(host, username, password, finish, DataCenter_RtspServer0Command)
            rtsp_server_0_fifo_addr, rtsp_server_0_cur_num, rtsp_server_0_max_cur_num, rtsp_server_0_drop_num = collectDataCenter_Rtsp_server_0(DataCenter_Rtsp_server0)

            DataCenter_Rtsp_server1 = do_telnet(host, username, password, finish, DataCenter_RtspServer1Command)
            rtsp_server_1_fifo_addr, rtsp_server_1_cur_num, rtsp_server_1_max_cur_num, rtsp_server_1_drop_num = collectDataCenter_Rtsp_server_1(DataCenter_Rtsp_server1)

            DataCenter_Rtsp_server2 = do_telnet(host, username, password, finish, DataCenter_RtspServer2Command)
            rtsp_server_2_fifo_addr, rtsp_server_2_cur_num, rtsp_server_2_max_cur_num, rtsp_server_2_drop_num = collectDataCenter_Rtsp_server_2(DataCenter_Rtsp_server2)

            DataCenter_Rtsp_server3 = do_telnet(host, username, password, finish, DataCenter_RtspServer3Command)
            rtsp_server_3_fifo_addr, rtsp_server_3_cur_num, rtsp_server_3_max_cur_num, rtsp_server_3_drop_num = collectDataCenter_Rtsp_server_3(DataCenter_Rtsp_server3)

            DataCenter_Rtsp_server4 = do_telnet(host, username, password, finish, DataCenter_RtspServer4Command)
            rtsp_server_4_fifo_addr, rtsp_server_4_cur_num, rtsp_server_4_max_cur_num, rtsp_server_4_drop_num = collectDataCenter_Rtsp_server_4(DataCenter_Rtsp_server4)

            DataCenter_Rtsp_server5 = do_telnet(host, username, password, finish, DataCenter_RtspServer5Command)
            rtsp_server_5_fifo_addr, rtsp_server_5_cur_num, rtsp_server_5_max_cur_num, rtsp_server_5_drop_num = collectDataCenter_Rtsp_server_5(DataCenter_Rtsp_server5)

            DataCenter_Rtsp_server6 = do_telnet(host, username, password, finish, DataCenter_RtspServer6Command)
            rtsp_server_6_fifo_addr, rtsp_server_6_cur_num, rtsp_server_6_max_cur_num, rtsp_server_6_drop_num = collectDataCenter_Rtsp_server_6(DataCenter_Rtsp_server6)

            DataCenter_Rtsp_server7 = do_telnet(host, username, password, finish, DataCenter_RtspServer7Command)
            rtsp_server_7_fifo_addr, rtsp_server_7_cur_num, rtsp_server_7_max_cur_num, rtsp_server_7_drop_num = collectDataCenter_Rtsp_server_7(DataCenter_Rtsp_server7)

            DataCenter_Rtsp_server8 = do_telnet(host, username, password, finish, DataCenter_RtspServer8Command)
            rtsp_server_8_fifo_addr, rtsp_server_8_cur_num, rtsp_server_8_max_cur_num, rtsp_server_8_drop_num = collectDataCenter_Rtsp_server_8(DataCenter_Rtsp_server8)

            DataCenter_Rtsp_server9 = do_telnet(host, username, password, finish, DataCenter_RtspServer9Command)
            rtsp_server_9_fifo_addr, rtsp_server_9_cur_num, rtsp_server_9_max_cur_num, rtsp_server_9_drop_num = collectDataCenter_Rtsp_server_9(DataCenter_Rtsp_server9)

            DataCenter_Rtsp_server10 = do_telnet(host, username, password, finish, DataCenter_RtspServer10Command)
            rtsp_server_10_fifo_addr, rtsp_server_10_cur_num, rtsp_server_10_max_cur_num, rtsp_server_10_drop_num = collectDataCenter_Rtsp_server_10(DataCenter_Rtsp_server10)

            DataCenter_Rtsp_server11 = do_telnet(host, username, password, finish, DataCenter_RtspServer11Command)
            rtsp_server_11_fifo_addr, rtsp_server_11_cur_num, rtsp_server_11_max_cur_num, rtsp_server_11_drop_num = collectDataCenter_Rtsp_server_11(DataCenter_Rtsp_server11)

            DataCenter_Rtsp_server12 = do_telnet(host, username, password, finish, DataCenter_RtspServer12Command)
            rtsp_server_12_fifo_addr, rtsp_server_12_cur_num, rtsp_server_12_max_cur_num, rtsp_server_12_drop_num = collectDataCenter_Rtsp_server_12(DataCenter_Rtsp_server12)

            DataCenter_Rtsp_server13 = do_telnet(host, username, password, finish, DataCenter_RtspServer13Command)
            rtsp_server_13_fifo_addr, rtsp_server_13_cur_num, rtsp_server_13_max_cur_num, rtsp_server_13_drop_num = collectDataCenter_Rtsp_server_13(DataCenter_Rtsp_server13)

            DataCenter_Rtsp_server14 = do_telnet(host, username, password, finish, DataCenter_RtspServer14Command)
            rtsp_server_14_fifo_addr, rtsp_server_14_cur_num, rtsp_server_14_max_cur_num, rtsp_server_14_drop_num = collectDataCenter_Rtsp_server_14(DataCenter_Rtsp_server14)

            DataCenter_Rtsp_server15 = do_telnet(host, username, password, finish, DataCenter_RtspServer15Command)
            rtsp_server_15_fifo_addr, rtsp_server_15_cur_num, rtsp_server_15_max_cur_num, rtsp_server_15_drop_num = collectDataCenter_Rtsp_server_15(DataCenter_Rtsp_server15)


            DataCenter_Rtsp_client0 = do_telnet(host, username, password, finish, DataCenter_RtspClient0Command)
            rtsp_client_0_fifo_addr, rtsp_client_0_cur_num, rtsp_client_0_max_cur_num, rtsp_client_0_drop_num = collectDataCenter_Rtsp_client_0(DataCenter_Rtsp_client0)

            DataCenter_Rtsp_client1 = do_telnet(host, username, password, finish, DataCenter_RtspClient1Command)
            rtsp_client_1_fifo_addr, rtsp_client_1_cur_num, rtsp_client_1_max_cur_num, rtsp_client_1_drop_num = collectDataCenter_Rtsp_client_1(DataCenter_Rtsp_client1)

            DataCenter_Rtsp_client2 = do_telnet(host, username, password, finish, DataCenter_RtspClient2Command)
            rtsp_client_2_fifo_addr, rtsp_client_2_cur_num, rtsp_client_2_max_cur_num, rtsp_client_2_drop_num = collectDataCenter_Rtsp_client_2(DataCenter_Rtsp_client2)

            DataCenter_Rtsp_client3 = do_telnet(host, username, password, finish, DataCenter_RtspClient3Command)
            rtsp_client_3_fifo_addr, rtsp_client_3_cur_num, rtsp_client_3_max_cur_num, rtsp_client_3_drop_num = collectDataCenter_Rtsp_client_3(DataCenter_Rtsp_client3)

            DataCenter_Rtsp_client4 = do_telnet(host, username, password, finish, DataCenter_RtspClient4Command)
            rtsp_client_4_fifo_addr, rtsp_client_4_cur_num, rtsp_client_4_max_cur_num, rtsp_client_4_drop_num = collectDataCenter_Rtsp_client_4(DataCenter_Rtsp_client4)

            DataCenter_Rtsp_client5 = do_telnet(host, username, password, finish, DataCenter_RtspClient5Command)
            rtsp_client_5_fifo_addr, rtsp_client_5_cur_num, rtsp_client_5_max_cur_num, rtsp_client_5_drop_num = collectDataCenter_Rtsp_client_5(DataCenter_Rtsp_client5)

            DataCenter_Rtsp_client6 = do_telnet(host, username, password, finish, DataCenter_RtspClient6Command)
            rtsp_client_6_fifo_addr, rtsp_client_6_cur_num, rtsp_client_6_max_cur_num, rtsp_client_6_drop_num = collectDataCenter_Rtsp_client_6(DataCenter_Rtsp_client6)

            DataCenter_Rtsp_client7 = do_telnet(host, username, password, finish, DataCenter_RtspClient7Command)
            rtsp_client_7_fifo_addr, rtsp_client_7_cur_num, rtsp_client_7_max_cur_num, rtsp_client_7_drop_num = collectDataCenter_Rtsp_client_7(DataCenter_Rtsp_client7)

            DataCenter_Rtsp_client8 = do_telnet(host, username, password, finish, DataCenter_RtspClient8Command)
            rtsp_client_8_fifo_addr, rtsp_client_8_cur_num, rtsp_client_8_max_cur_num, rtsp_client_8_drop_num = collectDataCenter_Rtsp_client_8(DataCenter_Rtsp_client8)

            DataCenter_Rtsp_client9 = do_telnet(host, username, password, finish, DataCenter_RtspClient9Command)
            rtsp_client_9_fifo_addr, rtsp_client_9_cur_num, rtsp_client_9_max_cur_num, rtsp_client_9_drop_num = collectDataCenter_Rtsp_client_9(DataCenter_Rtsp_client9)

            DataCenter_Rtsp_client10 = do_telnet(host, username, password, finish, DataCenter_RtspClient10Command)
            rtsp_client_10_fifo_addr, rtsp_client_10_cur_num, rtsp_client_10_max_cur_num, rtsp_client_10_drop_num = collectDataCenter_Rtsp_client_10(DataCenter_Rtsp_client10)

            DataCenter_Rtsp_client11 = do_telnet(host, username, password, finish, DataCenter_RtspClient11Command)
            rtsp_client_11_fifo_addr, rtsp_client_11_cur_num, rtsp_client_11_max_cur_num, rtsp_client_11_drop_num = collectDataCenter_Rtsp_client_11(DataCenter_Rtsp_client11)

            DataCenter_Rtsp_client12 = do_telnet(host, username, password, finish, DataCenter_RtspClient12Command)
            rtsp_client_12_fifo_addr, rtsp_client_12_cur_num, rtsp_client_12_max_cur_num, rtsp_client_12_drop_num = collectDataCenter_Rtsp_client_12(DataCenter_Rtsp_client12)

            DataCenter_Rtsp_client13 = do_telnet(host, username, password, finish, DataCenter_RtspClient13Command)
            rtsp_client_13_fifo_addr, rtsp_client_13_cur_num, rtsp_client_13_max_cur_num, rtsp_client_13_drop_num = collectDataCenter_Rtsp_client_13(DataCenter_Rtsp_client13)

            DataCenter_Rtsp_client14 = do_telnet(host, username, password, finish, DataCenter_RtspClient14Command)
            rtsp_client_14_fifo_addr, rtsp_client_14_cur_num, rtsp_client_14_max_cur_num, rtsp_client_14_drop_num = collectDataCenter_Rtsp_client_14(DataCenter_Rtsp_client14)

            DataCenter_Rtsp_client15 = do_telnet(host, username, password, finish, DataCenter_RtspClient15Command)
            rtsp_client_15_fifo_addr, rtsp_client_15_cur_num, rtsp_client_15_max_cur_num, rtsp_client_15_drop_num = collectDataCenter_Rtsp_client_14(DataCenter_Rtsp_client15)



            DataCenter_Rtsp_server_setsei = do_telnet(host, username, password, finish, DataCenter_RtspServerSetseiCommand)
            cur_num2, max_num2, max_cur_num2, pkg_mem_size2 = collectDataCenter_rtsp_server_setsei(DataCenter_Rtsp_server_setsei)

            DataCenter_web_server = do_telnet(host, username, password, finish, DataCenter_Web_ServerCommand)
            cur_num3, max_num3, max_cur_num3, pkg_mem_size3 = collectDataCenter_web_server(DataCenter_web_server)

            OutresUptime = do_telnet(host, username, password, finish, uptimeCommand)
            uptime= collectuptime(OutresUptime)

            #-----------------------------------------------------------


            client.write_points(CPU_DataToInfluxDB(host, userCpu, sysCpu, idleCpu, ioCpu))
            client.write_points(uptime_DataToInfluxDB(host, uptime))
            client.write_points(Mem_DataToInfluxDB(host,MemFree,MemTotal,Buffers,Cached,Vmrss))
            client.write_points(DataCenter_DataToInfluxDB(host,cur_num2,max_num2,max_cur_num2,pkg_mem_size2,cur_num3,max_num3,max_cur_num3,pkg_mem_size3))
            client.write_points(NNIE_DataToInfluxDB(host,CoreId0_CntPerSec,CoreId0_MaxCntPerSec,CoreId1_CntPerSec,CoreId1_MaxCntPerSec))
            client.write_points(Rtsp_server_fifo_addr_DataToInfluxDB(host, rtsp_server_0_fifo_addr,rtsp_server_1_fifo_addr,rtsp_server_2_fifo_addr,rtsp_server_3_fifo_addr,rtsp_server_4_fifo_addr,rtsp_server_5_fifo_addr,rtsp_server_6_fifo_addr,rtsp_server_7_fifo_addr,rtsp_server_8_fifo_addr,rtsp_server_9_fifo_addr,rtsp_server_10_fifo_addr,rtsp_server_11_fifo_addr,rtsp_server_12_fifo_addr,rtsp_server_13_fifo_addr,rtsp_server_14_fifo_addr,rtsp_server_15_fifo_addr))
            client.write_points(Rtsp_server_cur_num_DataToInfluxDB(host,rtsp_server_0_cur_num,rtsp_server_1_cur_num,rtsp_server_2_cur_num,rtsp_server_3_cur_num,rtsp_server_4_cur_num,rtsp_server_5_cur_num,rtsp_server_6_cur_num,rtsp_server_7_cur_num,rtsp_server_8_cur_num,rtsp_server_9_cur_num,rtsp_server_10_cur_num,rtsp_server_11_cur_num,rtsp_server_12_cur_num,rtsp_server_13_cur_num,rtsp_server_14_cur_num,rtsp_server_15_cur_num))
            # client.write_points(Rtsp_server_max_num_DataToInfluxDB(host,rtsp_server_0_max_num,rtsp_server_1_max_num,rtsp_server_2_max_num,rtsp_server_3_max_num, rtsp_server_4_max_num, rtsp_server_5_max_num,rtsp_server_6_max_num, rtsp_server_7_max_num, rtsp_server_8_max_num,rtsp_server_9_max_num, rtsp_server_10_max_num,rtsp_server_11_max_num,rtsp_server_12_max_num, rtsp_server_13_max_num,rtsp_server_14_max_num,rtsp_server_15_max_num))
            client.write_points(Rtsp_server_max_cur_num_DataToInfluxDB(host, rtsp_server_0_max_cur_num, rtsp_server_1_max_cur_num,rtsp_server_2_max_cur_num,rtsp_server_3_max_cur_num, rtsp_server_4_max_cur_num,
                                                       rtsp_server_5_max_cur_num,
                                                       rtsp_server_6_max_cur_num, rtsp_server_7_max_cur_num,
                                                       rtsp_server_8_max_cur_num,
                                                       rtsp_server_9_max_cur_num, rtsp_server_10_max_cur_num,
                                                       rtsp_server_11_max_cur_num,
                                                       rtsp_server_12_max_cur_num, rtsp_server_13_max_cur_num,
                                                       rtsp_server_14_max_cur_num,
                                                       rtsp_server_15_max_cur_num))
            client.write_points(Rtsp_server_drop_num_DataToInfluxDB(host, rtsp_server_0_drop_num, rtsp_server_1_drop_num,
                                                                    rtsp_server_2_drop_num, rtsp_server_3_drop_num,
                                                                    rtsp_server_4_drop_num, rtsp_server_5_drop_num,
                                                                    rtsp_server_6_drop_num, rtsp_server_7_drop_num,
                                                                    rtsp_server_8_drop_num, rtsp_server_9_drop_num,
                                                                    rtsp_server_10_drop_num, rtsp_server_11_drop_num,
                                                                    rtsp_server_12_drop_num, rtsp_server_13_drop_num,
                                                                    rtsp_server_14_drop_num, rtsp_server_15_drop_num))
            client.write_points(Rtsp_client_fifo_addr_DataToInfluxDB(host, rtsp_client_0_fifo_addr, rtsp_client_1_fifo_addr,
                                                                    rtsp_client_2_fifo_addr, rtsp_client_3_fifo_addr,
                                                                    rtsp_client_4_fifo_addr, rtsp_client_5_fifo_addr,
                                                                    rtsp_client_6_fifo_addr, rtsp_client_7_fifo_addr,
                                                                    rtsp_client_8_fifo_addr, rtsp_client_9_fifo_addr,
                                                                    rtsp_client_10_fifo_addr, rtsp_client_11_fifo_addr,
                                                                    rtsp_client_12_fifo_addr, rtsp_client_13_fifo_addr,
                                                                    rtsp_client_14_fifo_addr, rtsp_client_15_fifo_addr))
            client.write_points(Rtsp_client_cur_num_DataToInfluxDB(host, rtsp_client_0_cur_num, rtsp_client_1_cur_num,
                                                   rtsp_client_2_cur_num,
                                                   rtsp_client_3_cur_num, rtsp_client_4_cur_num, rtsp_client_5_cur_num,
                                                   rtsp_client_6_cur_num, rtsp_client_7_cur_num, rtsp_client_8_cur_num,
                                                   rtsp_client_9_cur_num, rtsp_client_10_cur_num,
                                                   rtsp_client_11_cur_num,
                                                   rtsp_client_12_cur_num, rtsp_client_13_cur_num,
                                                   rtsp_client_14_cur_num,
                                                   rtsp_client_15_cur_num))
            client.write_points(Rtsp_client_max_cur_num_DataToInfluxDB(host, rtsp_client_0_max_cur_num, rtsp_client_1_max_cur_num,
                                                       rtsp_client_2_max_cur_num,
                                                       rtsp_client_3_max_cur_num, rtsp_client_4_max_cur_num,
                                                       rtsp_client_5_max_cur_num,
                                                       rtsp_client_6_max_cur_num, rtsp_client_7_max_cur_num,
                                                       rtsp_client_8_max_cur_num,
                                                       rtsp_client_9_max_cur_num, rtsp_client_10_max_cur_num,
                                                       rtsp_client_11_max_cur_num,
                                                       rtsp_client_12_max_cur_num, rtsp_client_13_max_cur_num,
                                                       rtsp_client_14_max_cur_num,
                                                       rtsp_client_15_max_cur_num))
            client.write_points(Rtsp_client_drop_num_DataToInfluxDB(host, rtsp_client_0_drop_num, rtsp_client_1_drop_num,
                                                    rtsp_client_2_drop_num, rtsp_client_3_drop_num,
                                                    rtsp_client_4_drop_num, rtsp_client_5_drop_num,
                                                    rtsp_client_6_drop_num, rtsp_client_7_drop_num,
                                                    rtsp_client_8_drop_num, rtsp_client_9_drop_num,
                                                    rtsp_client_10_drop_num, rtsp_client_11_drop_num,
                                                    rtsp_client_12_drop_num, rtsp_client_13_drop_num,
                                                    rtsp_client_14_drop_num, rtsp_client_15_drop_num))
            num +=1
        except Exception as e:
            print("收集数据失败或异常：%s%s" % (host,e))
            traceback.print_exc()
            num += 1
            time.sleep(3)
            continue
        # else:
        #     time.sleep(10)

if __name__=='__main__':
     # 配置选项
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
    BoxIPList = ['10.58.122.205','10.58.122.215','10.58.122.201','10.58.122.108','10.58.122.237','10.58.122.221']

    dbhost= '10.58.150.5'
    username = b'root\n'   # 登录用户名
    password = b'HZ*SF#ai1xS!\n'  # 登录密码
    #finish = 'LEVEL COMMAND <___>'      # 命令提示符
    finish = b'~ #'  # 命令提示符
    # userCpuList = []

    cpuInfoCommand = b'top -n1 | head -n2 | tail -n1;exit\n'
    memFreeCommand = b'cat /proc/meminfo;exit\n'
    NNIECommand = b'cat /proc/umap/nnie | head -n 22 | tail -n +20;exit\n'
    BoxmainPidCommand = b'ps|grep -v grep|grep /usr/local/app/bin/BoxMain;exit\n'
# -------------------------16个通道--------------------------------------
    DataCenter_RtspServer0Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_0;exit\n'
    DataCenter_RtspServer1Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_1;exit\n'
    DataCenter_RtspServer2Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_2;exit\n'
    DataCenter_RtspServer3Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_3;exit\n'
    DataCenter_RtspServer4Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_4;exit\n'
    DataCenter_RtspServer5Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_5;exit\n'
    DataCenter_RtspServer6Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_6;exit\n'
    DataCenter_RtspServer7Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_7;exit\n'
    DataCenter_RtspServer8Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_8;exit\n'
    DataCenter_RtspServer9Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_9;exit\n'
    DataCenter_RtspServer10Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_10;exit\n'
    DataCenter_RtspServer11Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_11;exit\n'
    DataCenter_RtspServer12Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_12;exit\n'
    DataCenter_RtspServer13Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_13;exit\n'
    DataCenter_RtspServer14Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_14;exit\n'
    DataCenter_RtspServer15Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_15;exit\n'
# ---------------------------------------------16------------------------------------------------
    DataCenter_RtspClient0Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_0;exit\n'
    DataCenter_RtspClient1Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_1;exit\n'
    DataCenter_RtspClient2Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_2;exit\n'
    DataCenter_RtspClient3Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_3;exit\n'
    DataCenter_RtspClient4Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_4;exit\n'
    DataCenter_RtspClient5Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_5;exit\n'
    DataCenter_RtspClient6Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_6;exit\n'
    DataCenter_RtspClient7Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_7;exit\n'
    DataCenter_RtspClient8Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_8;exit\n'
    DataCenter_RtspClient9Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_9;exit\n'
    DataCenter_RtspClient10Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_10;exit\n'
    DataCenter_RtspClient11Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_11;exit\n'
    DataCenter_RtspClient12Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_12;exit\n'
    DataCenter_RtspClient13Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_13;exit\n'
    DataCenter_RtspClient14Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_14;exit\n'
    DataCenter_RtspClient15Command = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client_15;exit\n'

    DataCenter_RtspServerSetseiCommand = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_setsei;exit\n'
    DataCenter_Web_ServerCommand = b'cat /proc/rtinfo/datacenter |grep -w web_server;exit\n'
    uptimeCommand = b'uptime;exit\n'

    client = InfluxDBClient(dbhost, 8086, database="iboxmonitoring")
    for ip in BoxIPList:
        try:
            ip = threading.Thread(target=run,args=(ip,))
            ip.start()
        except Exception as e:
            print(ip,":收集数据线程启动失败，重新启动线程继续收集数据")