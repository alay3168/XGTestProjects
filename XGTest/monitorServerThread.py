#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     :
# @Version    : 1.0
# @Date       :
# @Description: Momitor
#****************************************************************

import logging
import threading
import time

import paramiko
from influxdb import InfluxDBClient

LOGGER = logging.getLogger("monitor")

def pfloat(p):
    return float(p.replace('%', ''))

def do_ssh(Host, username, password, cmd):
    # 创建一个ssh的客户端，用来连接服务器
    ssh = paramiko.SSHClient()
    # 创建一个ssh的白名单
    know_host = paramiko.AutoAddPolicy()
    # 加载创建的白名单
    ssh.set_missing_host_key_policy(know_host)
    # 连接服务器
    ssh.connect(
        hostname=Host,
        port=22,
        username=username,
        password=password
    )
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    #获取命令执行结果
    Outres = stdout.read().decode()
    ssh.close()
    return Outres

def collectCpuinfo(OutresCpuInfo):
    CpuInfo_list = OutresCpuInfo
    CPU_list = CpuInfo_list.split()
    userCpuValue = pfloat(CPU_list[9])
    sysCpuValue = pfloat(CPU_list[11])
    idleCpuValue = pfloat(CPU_list[15])
    ioValue = pfloat(CPU_list[17])
    return (userCpuValue,sysCpuValue,idleCpuValue,ioValue)

def collectMemFree(OutresMemFree):
    lines = OutresMemFree.splitlines()
    lines = [line.split(":") for line in lines if ":" in line]
    lines = [(k, int(v.strip().split(' ')[0])) for [k,v] in lines]
    data = dict(lines)
    return data["MemFree"], data["MemTotal"], data["Buffers"], data["Cached"]

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

def Mem_DataToInfluxDB(Host,MemFree,MemTotal,Buffers,Cached):
    data_list = [{
        'measurement': 'Memory',
        'tags': {'deviceIP': Host},
        'fields': {
            'MemFree': MemFree,
            'MemTotal' : MemTotal,
            'Buffers': Buffers,
            'Cached' : Cached
        },
    }]
    return data_list


def run(Host):
    host = Host
    while True:
        try:
            OutresCpuInfo = do_ssh(host, username, password, cpuInfoCommand)
            userCpu, sysCpu, idleCpu, ioCpu = collectCpuinfo(OutresCpuInfo)

            OutresMemFree = do_ssh(host, username, password, memFreeCommand)
            MemFree,MemTotal,Buffers,Cached= collectMemFree(OutresMemFree)

            client.write_points(CPU_DataToInfluxDB(host, userCpu, sysCpu, idleCpu, ioCpu))
            client.write_points(Mem_DataToInfluxDB(host,MemFree,MemTotal,Buffers,Cached))

        except Exception as e:
            print("收集数据失败或异常：%s%s" % (host,e))
            time.sleep(3)
            continue
        # else:
        #     time.sleep(10)

if __name__=='__main__':
     # 配置选项
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
    serverIPList = ['10.58.150.6']
    username = b'root\n'  # 登录用户名
    password = b'1qaz3edc\n'  # 登录密码
    cpuInfoCommand = b'top -n2 | head -n3 | tail -n1;exit\n'
    memFreeCommand = b'cat /proc/meminfo;exit\n'
    nvidiaCommand = b'nvidia-smi;exit\n'

    dbhost = '10.58.150.5'
    client = InfluxDBClient(dbhost, 8086, database="servermonitoring")
    for ip in serverIPList:
        try:
            ip = threading.Thread(target=run,args=(ip,))
            ip.start()
        except Exception as e:
            print(ip,":收集数据线程启动失败，重新启动线程继续收集数据")
