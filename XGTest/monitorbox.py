#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************
# @Author     :
# @Version    : 1.0
# @Date       :
# @Description: Momitor
# ****************************************************************

import telnetlib
import time

from influxdb import InfluxDBClient


def pfloat(p):
    return float(p.replace('%', ''))


def do_telnet(Host, username, password, finish, cmds):
    # 连接Telnet服务器
    tn = telnetlib.Telnet(Host, port=23, timeout=10)
    tn.set_debuglevel(2)

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
    #     result = tn.write('%s\r\n' % command);
    # 执行结果保存至文件
    Outres = tn.read_all()
    return Outres


def collectCpuinfo(OutresCpuInfo):
    # OutresCpuInfo = str(OutresCpuInfo, encoding="utf-8")

    # OutresCpuInfo = OutresCpuInfo.split('\r\n')
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
    return (userCpuValue, sysCpuValue, idleCpuValue, ioValue)


def collectMemFree(OutresMemFree):
    OutresMemFree = str(OutresMemFree)
    OutresMemFree = OutresMemFree.split('\r\n')
    OutresMemFree = OutresMemFree[1:len(OutresMemFree) - 1]
    OutresMemFree = dict(map(lambda x: x.split(':'), OutresMemFree))
    MemFreeValue = int(OutresMemFree['MemFree'].split()[0])
    return MemFreeValue


def GetBoxMain_pid():
    BoxmianPid_List = str(Boxmain).split('\r\n')
    print(BoxmianPid_List)
    BoxmianPid = BoxmianPid_List[1].split()[0]

    return BoxmianPid


def collectVMRss(OutresVmRSS):
    OutresVmRSS = str(OutresVmRSS)
    OutresVmRSS = OutresVmRSS.split('\r\n')
    OutresVmRSS = OutresVmRSS[1:len(OutresVmRSS) - 1]
    OutresVmRSS = dict(map(lambda x: x.split(':'), OutresVmRSS))
    VmRSSValue = int(OutresVmRSS['VmRSS'].split()[0])
    return VmRSSValue


def collectDataCenter_Rtsp_server(DataCenter_Rtsp_server):
    Rtsp_server_list = str(DataCenter_Rtsp_server).split('\r\n')
    cur_numValue = int(Rtsp_server_list[1].split()[2])
    max_numValue = int(Rtsp_server_list[1].split()[3])
    max_cur_numValue = int(Rtsp_server_list[1].split()[4])
    pkg_mem_sizeValue = int(Rtsp_server_list[1].split()[5])

    return (cur_numValue, max_numValue, max_cur_numValue, pkg_mem_sizeValue)


def collectDataCenter_rtsp_client(DataCenter_rtsp_client):
    rtsp_client_list = str(DataCenter_rtsp_client).split('\r\n')
    cur_numValue = int(rtsp_client_list[2].split()[2])
    max_numValue = int(rtsp_client_list[2].split()[3])
    max_cur_numValue = int(rtsp_client_list[2].split()[4])
    pkg_mem_sizeValue = int(rtsp_client_list[2].split()[5])

    return (cur_numValue, max_numValue, max_cur_numValue, pkg_mem_sizeValue)


def collectDataCenter_rtsp_server_setsei(DataCenter_rtsp_server_setsei):
    rtsp_server_setsei_list = str(DataCenter_rtsp_server_setsei).split('\r\n')
    cur_numValue = int(rtsp_server_setsei_list[1].split()[2])
    max_numValue = int(rtsp_server_setsei_list[1].split()[3])
    max_cur_numValue = int(rtsp_server_setsei_list[1].split()[4])
    pkg_mem_sizeValue = int(rtsp_server_setsei_list[1].split()[5])

    return (cur_numValue, max_numValue, max_cur_numValue, pkg_mem_sizeValue)


def collectDataCenter_web_server(DataCenter_web_server):
    DataCenter_web_server_list = str(DataCenter_web_server).split('\r\n')
    cur_numValue = int(DataCenter_web_server_list[1].split()[2])
    max_numValue = int(DataCenter_web_server_list[1].split()[3])
    max_cur_numValue = int(DataCenter_web_server_list[1].split()[4])
    pkg_mem_sizeValue = int(DataCenter_web_server_list[1].split()[5])

    return (cur_numValue, max_numValue, max_cur_numValue, pkg_mem_sizeValue)


def CPU_DataToInfluxDB(Host, userCpu, sysCpu, idleCpu, ioCpu):
    # now = datetime.datetime.now()
    # t = datetime.datetime.fromtimestamp(now.timestamp()).isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
    data_list = [{
        'measurement': 'CPU',
        'tags': {'deviceIP': Host},
        'fields': {
            'userCpu': userCpu,
            'sysCpu': sysCpu,
            'idelCpu': idleCpu,
            'ioCpu': ioCpu
        },
    }]
    return data_list


# def Mem_DataToInfluxDB(Host,MemFree,Vmrss):
def Mem_DataToInfluxDB():
    # now = datetime.datetime.now()
    # t = datetime.datetime.fromtimestamp(now.timestamp()).isoformat() #.strftime("%Y-%m-%dT%H:%M:%SZ")
    data_list = [{
        'measurement': 'Memory',
        'tags': {'deviceIP': Host},
        'fields': {
            'sysMemFree': MemFree,
            'ProVmrss': Vmrss
        },
    }]
    return data_list


def DataCenter_DataToInfluxDB():
    data_list = [{
        'measurement': 'DataCenter',
        'tags': {'deviceIP': Host},
        'fields': {
            'Rtspserver_curnum': cur_num,
            'Rtspserver_max_num': max_num,
            'Rtspserver_max_cur_num': max_cur_num,
            'Rtspserver_pkg_mem_size': pkg_mem_size,
            'Rtspclient_cur_num': cur_num1,
            'Rtspclient_max_num': max_num1,
            'Rtspclient_max_cur_num': max_cur_num1,
            'Rtspclient_pkg_mem_size': pkg_mem_size1,
            'Rtspserversetsei_cur_num': cur_num2,
            'Rtspserversetsei_max_num': max_num2,
            'Rtspserversetsei_max_cur_num': max_cur_num2,
            'Rtspserversetsei_pkg_mem_size_size': pkg_mem_size2,
            'WebServe_cur_num': cur_num3,
            'WebServe_cur_num_max_num': max_num3,
            'WebServe_cur_num_max_cur_num': max_cur_num3,
            'WebServe_cur_num_pkg_mem_size': pkg_mem_size3,
        },
    }]
    return data_list


if __name__ == '__main__':
    # 配置选项

    Host = '10.58.122.205'  # Telnet服务器IP
    username = b'root\n'  # 登录用户名
    password = b'HZ*SF#ai1xS!\n'  # 登录密码
    # finish = 'LEVEL COMMAND <___>'      # 命令提示符
    finish = b'~ #'  # 命令提示符
    # userCpuList = []

    cpuInfoCommand = b'top -n1 | head -n2 | tail -n1;exit\n'
    memFreeCommand = b'cat /proc/meminfo;exit\n'
    BoxmainPidCommand = b'ps|grep -v grep|grep /usr/local/app/bin/BoxMain;exit\n'
    Boxmain = do_telnet(Host, username, password, finish, BoxmainPidCommand)
    # BoxmianPid_List = str(Boxmain).split('\r\n')
    # BoxmianPid = BoxmianPid_List[1].split()[0]
    BoxmianPid = GetBoxMain_pid()
    VmRSSCommand = bytes("cat /proc/%s/status;exit\n" % BoxmianPid)
    NNIECommand = b'cat /proc/umap/nnie | head -n 12 | tail -n +9;exit\n'
    DataCenter_RtspServerCommand = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server;exit\n'
    DataCenter_RtspClientCommand = b'cat /proc/rtinfo/datacenter |grep -w rtsp_client;exit\n'
    DataCenter_RtspServerSetseiCommand = b'cat /proc/rtinfo/datacenter |grep -w rtsp_server_setsei;exit\n'
    DataCenter_Web_ServerCommand = b'cat /proc/rtinfo/datacenter |grep -w web_server;exit\n'
    monitor_log_error = b'tail -f /tmp/log/monitor.log | grep err;exit\n'
    # userCpulist = []
    # sysCpulist = []
    # idleCpulist = []
    # ioCpulist = []
    # MemFreelist = []
    # Vmrsslist = []
    # Rtspserver_cur_num =[]
    # Rtspserver_max_num = []
    # Rtspserver_max_cur_num = []
    # Rtspserver_pkg_mem_size= []
    # Rtspclient_cur_num = []
    # Rtspclient_max_num = []
    # Rtspclient_max_cur_num = []
    # Rtspclient_pkg_mem_size = []
    # Rtspserversetsei_cur_num = []
    # Rtspserversetsei_max_num = []
    # Rtspserversetsei_max_cur_num = []
    # Rtspserversetsei_pkg_mem_size = []
    # webServer_cur_num = []
    # webServer_max_num = []
    # webServer_max_cur_num = []
    # webServer_pkg_mem_size = []

    client = InfluxDBClient(Host, 8086, database="iboxmonitoring")

    while True:
        OutresCpuInfo = do_telnet(Host, username, password, finish, cpuInfoCommand)
        userCpu, sysCpu, idleCpu, ioCpu = collectCpuinfo(OutresCpuInfo)
        # print userCpu, sysCpu, idleCpu,ioCpu

        OutresMemFree = do_telnet(Host, username, password, finish, memFreeCommand)
        MemFree = collectMemFree(OutresMemFree)
        # print MemFree

        OutresVmRSS = do_telnet(Host, username, password, finish, VmRSSCommand)
        Vmrss = collectVMRss(OutresVmRSS)
        # print Vmrss

        DataCenter_Rtsp_server = do_telnet(Host, username, password, finish, DataCenter_RtspServerCommand)
        cur_num, max_num, max_cur_num, pkg_mem_size = collectDataCenter_Rtsp_server(DataCenter_Rtsp_server)
        # print cur_num,max_num,max_cur_num,pkg_mem_size

        DataCenter_Rtsp_client = do_telnet(Host, username, password, finish, DataCenter_RtspClientCommand)
        cur_num1, max_num1, max_cur_num1, pkg_mem_size1 = collectDataCenter_rtsp_client(DataCenter_Rtsp_client)
        # print cur_num1, max_num1, max_cur_num1, pkg_mem_size1

        DataCenter_Rtsp_server_setsei = do_telnet(Host, username, password, finish, DataCenter_RtspServerSetseiCommand)
        cur_num2, max_num2, max_cur_num2, pkg_mem_size2 = collectDataCenter_rtsp_server_setsei(
            DataCenter_Rtsp_server_setsei)
        # print cur_num2, max_num2, max_cur_num2, pkg_mem_size2

        DataCenter_web_server = do_telnet(Host, username, password, finish, DataCenter_Web_ServerCommand)
        cur_num3, max_num3, max_cur_num3, pkg_mem_size3 = collectDataCenter_web_server(DataCenter_web_server)
        # print cur_num3, max_num3, max_cur_num3, pkg_mem_size3

        # userCpulist.append(userCpu)
        # sysCpulist.append(sysCpu)
        # idleCpulist.append(idleCpu)
        # ioCpulist.append(ioCpu)
        # MemFreelist.append(MemFree)
        # Vmrsslist.append(Vmrss)
        # Rtspserver_cur_num.append(cur_num)
        # Rtspserver_max_num.append(max_num)
        # Rtspserver_max_cur_num.append(max_cur_num)
        # Rtspserver_pkg_mem_size.append(pkg_mem_size)
        # Rtspclient_cur_num.append(cur_num1)
        # Rtspclient_max_num.append(max_num1)
        # Rtspclient_max_cur_num.append(max_cur_num1)
        # Rtspclient_pkg_mem_size.append(pkg_mem_size1)
        # Rtspserversetsei_cur_num.append(cur_num2)
        # Rtspserversetsei_max_num.append(max_num2)
        # Rtspserversetsei_max_cur_num.append(max_cur_num2)
        # Rtspserversetsei_pkg_mem_size.append(pkg_mem_size2)
        # webServer_cur_num.append(cur_num3)
        # webServer_max_num.append(max_num3)
        # webServer_max_cur_num.append(max_cur_num3)
        # webServer_pkg_mem_size.append(pkg_mem_size3)

        client.write_points(CPU_DataToInfluxDB(Host, userCpu, sysCpu, idleCpu, ioCpu))
        client.write_points(Mem_DataToInfluxDB())
        client.write_points(DataCenter_DataToInfluxDB())

        time.sleep(5)
    # userCpuList.append(userCpu)
    # do_telnet(Host, username, password, finish, cmds)
