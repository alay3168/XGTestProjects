#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging
import telnetlib
import time
import traceback
import cv2
from influxdb import InfluxDBClient
import multiprocessing
import gc
import queue

LOGGER = logging.getLogger("monitor")
class CameraMonitor():
    def pfloat(self,p):
        return float(p.replace('%', ''))

    def do_telnet(self,Host, username, password, finish, cmds):
        # 连接Telnet服务器
        tn = telnetlib.Telnet(Host, port=23, timeout=60)
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
        #     result = tn.write('%s \\r\\n' % command);
        # 执行结果保存至文件
        Outres = tn.read_all()
        tn.close()
        return Outres

    def collectCpuinfo(self,OutresCpuInfo):
        # OutresCpuInfo = str(OutresCpuInfo, encoding="utf-8")

        # OutresCpuInfo = OutresCpuInfo.split(' \\r\\n')
        CpuInfo_list = str(OutresCpuInfo)
        CPU_list = CpuInfo_list.split()
        # OutresCpuInfo = OutresCpuInfo[3:5][1].split()
        # userCpuValue = float(CPU_list[9])
        userCpuValue = self.pfloat(CPU_list[9])
        sysCpuValue = self.pfloat(CPU_list[11])
        idleCpuValue = self.pfloat(CPU_list[15])
        ioValue = self.pfloat(CPU_list[17])
        # sysCpuValue = float(OutresCpuInfo[4])
        # delCpuValue = float(OutresCpuInfo[10])
        # return userCpuValue
        return (userCpuValue,sysCpuValue,idleCpuValue,ioValue)

    def collectMemFree(self,OutresMemFree):
        OutresMemFree = OutresMemFree.decode('utf-8')
        lines = OutresMemFree.splitlines()
        lines = [line.split(":") for line in lines if ":" in line]
        lines = [(k, int(v.strip().split(' ')[0])) for [k,v] in lines]
        data = dict(lines)
        return data["MemFree"], data["MemTotal"], data["Buffers"], data["Cached"]

    def Getpid(self,Boxmain):
        BoxmianPid_List = str(Boxmain).split()
        BoxmianPid = BoxmianPid_List[5]
        return BoxmianPid

    def collectVMRss(self,OutresVmRSS):
        OutresVmRSS = str(OutresVmRSS)
        OutresVmRSS = OutresVmRSS.split('\\r\\n')
        OutresVmRSS = OutresVmRSS[1:len(OutresVmRSS)-1]
        OutresVmRSS = dict(map(lambda x: x.split(':'), OutresVmRSS))
        VmRSSValue = int(OutresVmRSS['VmRSS'].split()[0])
        return VmRSSValue

    def getRtstFPS(self,IP):
        # video = cv2.VideoCapture(0)
        rtspUrl = 'rtsp://admin:123456@' + IP + '/MainStream'
        video = cv2.VideoCapture(rtspUrl)
        # Number of frames to capture
        num_frames = 250
        # Start time
        start = time.time()
        # Grab a few frames
        if video.isOpened():
            for i in range(0, num_frames):
                ret, frame = video.read()
                if ret == False:
                    seconds = time.time() - start
                    fps = i / seconds
                    video.release()
                    return fps
        else:
            video.release()
            return 0
        seconds = time.time() - start
        fps = num_frames / seconds
        # 释放 video
        video.release()
        print("Frame rate:", fps)
        return int(fps)

    #-------------------连接InfluxDB------------------------------
    def CPU_DataToInfluxDB(self,Host,userCpu,sysCpu,idleCpu,ioCpu):
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


    def Mem_DataToInfluxDB(self,Host,MemFree,MemTotal,Buffers,Cached):
        data_list = [{
            'measurement': 'Memory',
            'tags': {'deviceIP': Host},
            'fields': {
                'MemFree': MemFree,
                'MemTotal' : MemTotal,
                'Buffers': Buffers,
                'Cached' : Cached,
            },
        }]
        return data_list

    def Rtsp_DataToInfluxDB(self,Host,fps):
        data_list = [{
            'measurement': 'rtsp',
            'tags': {'deviceIP': Host},
            'fields': {
                'fps': fps,
            },
        }]
        return data_list

    def readIPCFile(self,ipfile):
        ipclist = []
        with open(ipfile, 'r') as f:
            ip = f.readlines()
        for i in range(len(ip)):
            ss = ip[i].split('\n')
            ipclist.append(ss[0])
        return ipclist

    def camera_capture_num(self):
        pass

    def run(self,Host):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
        host = Host
        username = b'root\n'  # 登录用户名
        password = b'XCM#ai18G!\n'  # 登录密码
        finish = b'~ #'  # 命令提示符

        cpuInfoCommand = b'top -n1 | head -n2 | tail -n1;exit\n'
        memFreeCommand = b'cat /proc/meminfo;exit\n'
        # NNIECommand = b'cat /proc/umap/nnie | head -n 22 | tail -n +20;exit\n'
        #mainPidCommand = b'ps|grep -v grep|grep /main/zxmain;exit\n'

        dbhost = '10.58.150.5'
        client = InfluxDBClient(dbhost, 8086, database="CameraMonitoring")
        # num = 1
        # maxnum =1
        while True :
            try:
                OutresCpuInfo = self.do_telnet(host, username, password, finish, cpuInfoCommand)
                userCpu, sysCpu, idleCpu, ioCpu = self.collectCpuinfo(OutresCpuInfo)

                OutresMemFree = self.do_telnet(host, username, password, finish, memFreeCommand)
                MemFree,MemTotal,Buffers,Cached= self.collectMemFree(OutresMemFree)

                rtsp = self.getRtstFPS(host)
                client.write_points(self.CPU_DataToInfluxDB(host, userCpu, sysCpu, idleCpu, ioCpu))
                client.write_points(self.Mem_DataToInfluxDB(host,MemFree,MemTotal,Buffers,Cached))
                client.write_points(self.Rtsp_DataToInfluxDB(host,rtsp))
                time.sleep(60)
                # num +=1
            except Exception as e:
                print("收集数据失败或异常：%s%s" % (host,e))
                traceback.print_exc()
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                time.sleep(3)
                # num +=1
                continue

if __name__=='__main__':
     # 配置选项
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
    cameraIpFile = 'cameraIp.txt'
    camera_monitor = CameraMonitor()
    cameraIPList = camera_monitor.readIPCFile(cameraIpFile)

    # cameraIPList = ['10.58.122.71', '10.58.122.72', '10.58.122.73', '10.58.122.74', '10.58.122.75','10.58.122.76','10.58.122.77','10.58.122.78','10.58.122.79','10.58.122.80','10.58.122.13','10.58.122.17','10.58.122.101','10.58.122.113','10.58.122.119','10.58.122.240','10.58.123.215','10.58.123.216','10.58.123.221','10.58.123.230','10.58.123.232','10.58.123.233','10.58.8.16','10.58.8.18','10.58.8.19',]
    for ip in cameraIPList:
        p = multiprocessing.Process(target=camera_monitor.run, args=(ip,))
        p.start()