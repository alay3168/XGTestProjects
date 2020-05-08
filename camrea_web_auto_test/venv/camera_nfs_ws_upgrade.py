#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import time
from datetime import datetime
from multiprocessing import Process

import telnetlib
import threading
import logging
import traceback
import random
import sys
from websocket import create_connection


# 登录接口请求函数
def Login(ip, ws, number):
    login_req = """{"Method":"Login","Page":"Login","Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}"""
    while True:
        print(str(datetime.now()) + "执行Login登录请求消息：", login_req)
        ws.send(login_req)  ##发送消息
        result = ws.recv()  ##接收消息
        result = json.loads(result)
        print(str(datetime.now()) + "执行Login登录返回消息：", result)
        if result["RetCode"] == 0:
            print(str(datetime.now()) + "：%s摄像机执行Login接口登录成功" % ip)
            break
        else:
            errorMessage = str(datetime.now()) + "：第%d次升级，%s摄像机执行Login接口登录失败返回信息：%s" % (number, ip, result)
            print(errorMessage)
            with open(autoUpdateFailLog, 'a') as f:
                f.write(errorMessage)
                f.write('\n')
            time.sleep(5)


# 执行开始升级接口请求函数
def UpgradeStar(ip, ws, filename, tolalSize, number):
    starUpdateReq = {"Method":"Maintain","Page":"Upgrade","Message":{"Status":"Start","File":"XG-IPC-1.0.10.20190531.tar","TotalSize":14929920,"PackSize":102400}}
    starUpdateReq["Message"]["File"] = filename
    starUpdateReq["Message"]["TotalSize"] = tolalSize
    starUpdateReqJosn = json.dumps(starUpdateReq)
    print(str(datetime.now()) + "执行UpgradeStar开始升级接口请求消息：", starUpdateReqJosn)
    ws.send(starUpdateReqJosn)  ##发送消息
    starUpdateRes = ws.recv()  ##接收消息#
    starUpdateRes = json.loads(starUpdateRes)
    print(str(datetime.now()) + "执行UpgradeStar开始升级接口返回消息：", starUpdateRes)
    RetCode = starUpdateRes["RetCode"]
    if RetCode != 0:
        errorMessage = str(datetime.now()) + "：第%d次升级，%s摄像机执行star接口开始传输升级包失败，其返回信息：%s，执行getlog.sh备份摄像机升级日志" % (
        number, ip, starUpdateRes)
        print(errorMessage)
        # cmd_res(ip, port, username, password, finish, cmds[2])
        # cmd_res(ip, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')
        # 发送transFinish清空摄像机升级状态
        transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                                "Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
        transFinishUpdateReq["Message"]["File"] = filename
        transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
        ws.send(transFinishUpdateReqJosn)
        return
    print(str(datetime.now()) + "：%s摄像机执行star接口开始传输升级包成功" % ip)


# 传输升级包接口请求函数
def UpgradeTrans(ip, ws, num, file, filename, endNum, number):
    PackNum = 1
    transUpdate = {"Method":"Maintain","Page":"Upgrade","Message":{"Status":"Trans","File":"XG-IPC-1.0.10.20190531.tar","CurSize":102400,"PackNum":1}}
    print(str(datetime.now()) + "：%s摄像机执行Trans接口开始发送升级包文件" % ip)
    while True:
        buf = file.read(102400)
        if num:
            transUpdate["Message"]["File"] = filename
            transUpdate["Message"]["PackNum"] = PackNum
            transUpdateReqJosn = json.dumps(transUpdate)
            transUpdateReq = bytes(transUpdateReqJosn, encoding='utf8') + bytes('\0', encoding='utf8') + buf
            # print('传输升级文件请求消息体：——————————————————————————%s'%transUpdateReq)
            time.sleep(1)
            # print(str(datetime.now()) + "执行UpgradeTrans传输升级包请求消息%d：%s" % (PackNum, transUpdateReq))
            ws.send(transUpdateReq)
            # print("-", end='')
            transUpdateReqRes = ws.recv()
            # print(str(datetime.now()) + "执行UpgradeTrans传输升级包响应消息%d：%s" % (PackNum, transUpdateReqRes))
            PackNum += 1
            num -= 1
        else:
            #print(str(datetime.now()) + "：%s摄像机传输最后一个升级包文件%d：" % (ip, PackNum))
            transUpdate["Message"]["File"] = filename
            transUpdate["Message"]["PackNum"] = PackNum
            transUpdate["Message"]["CurSize"] = endNum
            transUpdateReqJosn = json.dumps(transUpdate)
            transUpdateReqEnd = bytes(transUpdateReqJosn, encoding='utf8') + bytes('\0', encoding='utf8') + buf
            #print(str(datetime.now()) + "执行UpgradeTrans传输最后一个升级包请求消息%d：%s" % (PackNum, transUpdateReqEnd))
            ws.send(transUpdateReqEnd)
            transUpdateReqEndRes = ws.recv()
            print(
                str(datetime.now()) + "执行UpgradeTrans传输最后一个升级包响应消息%d：%s" % (PackNum, json.loads(transUpdateReqEndRes)))
            RetCode = json.loads(transUpdateReqEndRes)["RetCode"]
            if RetCode != 0:
                errorMessage = str(datetime.now()) + "：第%d次升级，%s摄像机执行Trans接口传输文件失败,其返回信息：%s，执行getlog.sh备份摄像机升级日志" % (
                number, ip, transUpdateReqEndRes)
                print(errorMessage)
                # cmd_res(ip, port, username, password, finish, cmds[2])
                # cmd_res(ip, port, username, password, finish, cmds[4])
                with open(autoUpdateFailLog, 'a') as f:
                    f.write(errorMessage)
                    f.write('\n')
                # 发送transFinish清空摄像机升级状态
                transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                                        "Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
                transFinishUpdateReq["Message"]["File"] = filename
                transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
                ws.send(transFinishUpdateReqJosn)
                return
            break
    print(str(datetime.now()) + "：%s摄像机执行Trans接口传输升级包文件完成" % ip)


# 发送传输文件完成却接口请求函数
def UpgradeTransFinish(ip, ws, filename, number):
    transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                            "Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
    transFinishUpdateReq["Message"]["File"] = filename
    transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
    print(str(datetime.now()) + "执行UpgradeTransFinish发送传输文件完成接口请求消息%s" % transFinishUpdateReqJosn)
    ws.send(transFinishUpdateReqJosn)
    starUpdateRes = ws.recv()
    starUpdateRes = json.loads(starUpdateRes)
    print(str(datetime.now()) + "执行UpgradeTransFinish发送传输文件完成接口响应消息%s" % starUpdateRes)
    if starUpdateRes["RetCode"] == 0:
        print(str(datetime.now()) + "：%s摄像机执行TransFinish接口确认传输完整升级包文件成功" % ip)
    else:
        errorMessage = str(datetime.now()) + "：第%d次升级，%s摄像机执行TransFinish接口确认传输完整升级包文件失败,其返回信息：%s，执行getlog.sh备份摄像机升级日志" % (
        number, ip, starUpdateRes)
        print(errorMessage)
        # cmd_res(ip, port, username, password, finish, cmds[2])
        # cmd_res(ip, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')
        # print(str(datetime.now())+"：第%d次升级，执行TransFinish接口确认传输完整升级包文件成功,其返回信息：%s"%(number,starUpdateRes))


# 开始传输文件执行升级
def Upgrade(ip, ws, filename, fileSize, number):
    file = open(filename, mode='rb')
    Num = fileSize // 102400
    endNum = fileSize % 102400
    UpgradeStar(ip, ws, filename, fileSize, number)
    UpgradeTrans(ip, ws, Num, file, filename, endNum, number)
    UpgradeTransFinish(ip, ws, filename, number)
    print(str(
                datetime.now()) +'传输文件完成后等待300秒')
    time.sleep(300)

def cmd_res(ip, port, username, password, finish, cmd):
    try:
        # print(str(datetime.now()) + "：尝试telnet登录%s摄像机" % ip)
        tn = telnetlib.Telnet(ip, port=port, timeout=180)
        tn.set_debuglevel(2)
    except Exception as e:
        print(str(datetime.now()) + "：尝试telnet登录%s摄像机失败：%s" % (ip, e))
        traceback.print_exc(file=open(autoUpdateFailLog, 'a'))
    else:
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username)
        # 输入登录密码
        tn.read_until(b'Password:')
        tn.write(password)
        tn.read_until(finish)
        tn.write(cmd)
        Outres = tn.read_all()
        tn.close()
        return Outres


def get_ipcam_md5(outres):
    res = str(outres)
    md5 = str(res).split('\\r\\n')[1].split(' ')[0]
    return md5


def get_version(outres):
    res = str(outres)
    li = res.split('&')
    version = li[4].split('=')
    return version[1]


def get_ipcam_main(outres):
    res = str(outres)
    li = res.split(' ')
    ipcam_main_pid = li[5]
    return ipcam_main_pid

def get_tar_md5(outres):
    res = str(outres)
    tar_md5 = res.split('\\r\\n')[1].split(' ')[0]
    return tar_md5

def get_telnet_stauts(ip, port):
    print(str(
                datetime.now()) + '获取摄像机%s telnet的状态'%ip)
    try:
        tn = telnetlib.Telnet(ip, port=port, timeout=180)
        if tn !=None:
            print(str(
                datetime.now())+ '摄像机%s 能正常telnet，可以持续后面的升级操作'%ip)
            tn.close()
            return True
    except Exception as e:
        print(str(
                datetime.now()) + '摄像机%s 不能正常telent，不进行后续升级操作，其telnet失败信息'%(ip))
        print(str(e))
        return False


def ws_upgrade(ip,num):
    print(str(datetime.now()) + '摄像机%s升级前先重启摄像机' % ip)
    websocketIP = "ws://" + ip + ":8000"
    ws = create_connection(websocketIP, timeout=180)
    Login(ip, ws, num)
    Upgrade(ip, ws, file1, file1Size, num)

    # 升级完成后获取升级后的版本、MD5值以及主进程PID
    resVersion = cmd_res(ip, port, username, password, finish, cmds[8])
    nVersion = get_version(resVersion)
    print(str(
                datetime.now())+'升级完成后获取的版本%s' % nVersion)
    resmd5 = cmd_res(ip, port, username, password, finish, cmds[0])
    nmd5 = get_ipcam_md5(resmd5)
    print(str(
                datetime.now())+'升级完成后获取的MD5%s' % nmd5)
    resPid = cmd_res(ip, port, username, password, finish, cmds[9])
    pid = get_ipcam_main(resPid)
    print(str(
                datetime.now())+'升级完成后获取的PID%s' % pid)
    print(nVersion,'----------',Version1)
    print(nmd5, '----------' ,version1_ipcam_main_Md5)
    if nVersion == Version1 and nmd5 == version1_ipcam_main_Md5 and len(pid)>0:
        print(str(
            datetime.now()) + '------------------------------摄像机%s第%d次升级成功，升级后的版本号：%s------------------------------' % (
              ip, num, nVersion))
        with open(autoUpdateFailLog, 'a') as f:
            f.write(str(
            datetime.now()) + '------------------------------摄像机%s第%d次升级成功，升级后的版本号：%s------------------------------' % (
              ip, num, nVersion))
            f.write('\r\n')
    else:
        print(str(
            datetime.now()) + '------------------------------摄像机%s第%d次升级失败，升级前的版本号：%s,升级后的版本号：%s------------------------------' % (
                  ip, num, Version2, nVersion))
        with open(autoUpdateFailLog, 'a') as f:
            f.write(str(
            datetime.now()) + '------------------------------摄像机%s第%d次升级失败，升级前的版本号：%s,升级后的版本号：%s------------------------------' % (
                  ip, num, Version2, nVersion))
            f.write('\r\n')

def nfs_upgrade(ip,num):
    print(str(datetime.now()) + '摄像机%s挂载NFS' % ip)
    cmd_res(ip, port, username, password, finish, cmds[2])

    time.sleep(3)
    print(str(datetime.now()) + '摄像机%s拷贝升级文件到/tmp/upload目录下' % ip)
    cmd_res(ip, port, username, password, finish, cmds[3])
    time.sleep(10)
    print(str(datetime.now()) + '摄像机%s拷贝升级文件到/tmp/upload目录下校验拷贝的文件正确性' % ip)
    md5 = cmd_res(ip, port, username, password, finish, cmds[4])
    tar_md5 = get_tar_md5(md5)
    if tar_md5 == file2MD5:
        print(str(datetime.now()) + '摄像机%s解压升级文件' % ip)
        cmd_res(ip, port, username, password, finish, cmds[5])
        time.sleep(10)
        print(str(datetime.now()) + '摄像机%s杀掉进程' % ip)
        cmd_res(ip, port, username, password, finish, cmds[6])

        print(str(datetime.now()) + '摄像机%s开始执行升级'% ip)
        cmd_res(ip, port, username, password, finish, cmds[7])
        print(str(
            datetime.now()) + '------------------------------摄像机%s第%d升级完成，等待摄像机重启------------------------------' % (
                  ip, num))
        time.sleep(60)

        # 升级完成后获取升级后的版本、MD5值以及主进程PID
        resVersion = cmd_res(ip, port, username, password, finish, cmds[8])
        nVersion = get_version(resVersion)
        print(str(
                datetime.now())+ '升级完成后获取的版本%s' % nVersion)
        resmd5 = cmd_res(ip, port, username, password, finish, cmds[0])
        nmd5 = get_ipcam_md5(resmd5)
        print(str(
                datetime.now()) + '升级完成后获取ipcam_main的MD5%s' % nmd5)
        resPid = cmd_res(ip, port, username, password, finish, cmds[9])
        pid = get_ipcam_main(resPid)
        print(str(
                datetime.now()) + '升级完成后获取ipcam_main的的PID%s' % pid)
        print(nVersion,'----------',Version2)
        print(nmd5, '----------' ,version2_ipcam_main_Md5)
        if nVersion == Version2 and nmd5 == version2_ipcam_main_Md5 and len(pid)>0:
            print(str(
                datetime.now()) + '------------------------------摄像机%s第%d次升级成功，升级前的版本号：%s,升级后的版本号：%s------------------------------' % (
                      ip, num, Version1, nVersion))
            with open(autoUpdateFailLog, 'a') as f:
                f.write(str(
                datetime.now()) + '------------------------------摄像机%s第%d次升级成功，升级前的版本号：%s,升级后的版本号：%s------------------------------' % (
                      ip, num, Version1, nVersion))
                f.write('\r\n')
        else:
            print(str(
                datetime.now()) + '------------------------------摄像机%s第%d次升级失败，升级前的版本号：%s,升级后的版本号：%s------------------------------' % (
                      ip, num, Version1, nVersion))
            with open(autoUpdateFailLog, 'a') as f:
                f.write(str(
                datetime.now()) + '------------------------------摄像机%s第%d次升级失败，升级前的版本号：%s,升级后的版本号：%s------------------------------' % (
                      ip, num, Version1, nVersion))
                f.write('\r\n')


def run(ip):
    num = 1
    while True:
        try:
            #尝试telnet
            tns = get_telnet_stauts(ip, port)
            if tns ==True:
                print(str(datetime.now()) + '升级前先重启摄像机%s' % ip)
                cmd_res(ip, port, username, password, finish, cmds[1])
                time.sleep(60)
                print(str(datetime.now()) + '先获取%s摄像机的软件版本' % ip)
                version = cmd_res(ip, port, username, password, finish, cmds[8])
                oldVerion = get_version(version)
                if oldVerion >= Version2:
                    print(str(
                datetime.now()) + "————————————————————————————%s摄像机当前版本%s已是最新版本，需要通过ws接口降低版本至%s————————————————————————————" % (
                    ip, oldVerion, Version1))
                    ws_upgrade(ip, num)
                    num = num + 1
                    # if num > 2:
                    #     break
                else:
                    print(str(
                datetime.now()) + "————————————————————————————摄像机%s开始升级Version2,其升级版本号是%s————————————————————————————" % (
                    ip, Version2))
                    print(
                        str(datetime.now()) + '------------------------------%s开始进行第%d次升级------------------------------' % (
                            ip, num))
                    nfs_upgrade(ip, num)
                    num = num + 1
                    # if num > 2:
                    #     break
            else:
                print(str(
                datetime.now()) + '将不升级的摄像机ip%s保存至upgrade_err_file文件中'%ip)
                with open(upgrade_err_file, 'a') as f:
                    f.write(ip)
                    f.write('\r\n')
        except Exception as e:
            print(str(
                datetime.now()) + "升级过程中出现异常，异常信息如下：—————————————————",e)
            traceback.print_exc()
            with open(autoUpdateFailLog, 'a') as f:
                f.write(str(e))
                traceback.print_exc(file=open(autoUpdateFailLog, 'a'))
                f.write('\r\n')
                continue

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
    ##案场：太原紫藤公馆 -----------------------
    # IPCList = ['10.10.40.247', '10.10.40.248', '10.10.40.246', '10.10.40.250', '10.10.40.251', '10.10.40.253', '10.10.40.249']

    # 案场：惠州木槿雅著 -----------------------
    # IPCList =['10.49.30.221', '10.49.30.226', '10.49.30.225', '10.49.30.223', '10.49.30.224', '10.49.30.222']

    # 案场：成都海棠名著 -----------------------
    # IPCList =['10.59.249.61', '10.59.249.62', '10.59.249.63', '10.59.249.64', '10.59.249.65', '10.59.249.66']

    # 案场：泰州君兰汀岸 -----------------------
    # IPCList =['172.168.20.225', '172.168.20.221', '172.168.20.228', '172.168.20.227', '172.168.20.226', '172.168.20.229']

    # 案场：遵义君兰国际 -----------------------
    # IPCList =['192.168.1.28', '192.168.1.9', '192.168.1.10', '192.168.1.117', '192.168.1.119', '192.168.1.116', '192.168.1.118',
    #  '192.168.1.12', '192.168.1.20', '192.168.1.14', '192.168.1.17', '192.168.1.15', '192.168.1.13', '192.168.1.21',
    #  '192.168.1.16', '192.168.1.19', '192.168.1.11', '192.168.1.18']

    # 案场：重庆永川蔷薇国际 -----------------------
    # IPCList =['172.168.100.201', '172.168.100.200', '172.168.100.213', '172.168.100.211', '172.168.100.209', '172.168.100.206',
    #  '172.168.100.204', '172.168.100.205', '172.168.100.203', '172.168.100.208', '172.168.100.214', '172.168.100.207',
    #  '172.168.100.202']

    # 案场：三亚海棠华著 -----------------------
    # IPCList =['192.168.1.33', '192.168.1.11', '192.168.1.44', '192.168.1.62', '192.168.1.41', '192.168.1.61']

    # 案场：常三 -----------------------
    # IPCList =['10.58.122.115', '10.58.122.56', '10.58.122.57', '10.58.122.52', '10.58.122.65', '10.58.122.64', '10.58.122.66',
    #  '10.58.122.69', '10.58.122.70', '10.58.122.71', '10.58.122.80', '10.58.122.92', '10.58.122.94', '10.58.122.93',
    #  '10.58.122.95', '10.58.122.202', '10.58.122.204', '10.58.122.203', '10.58.122.78', '10.58.122.101',
    #  '10.58.122.103', '10.58.122.116', '10.58.122.119', '10.58.122.73', '10.58.122.44', '10.58.122.105', '10.58.122.68',
    #  '10.58.122.108', '10.58.122.106', '10.58.122.207', '10.58.122.118', '10.58.122.91', '10.58.122.43', '10.58.122.99',
    #  '10.58.122.77', '10.58.122.79', '10.58.122.120', '10.58.122.59', '10.58.122.58', '10.58.122.50', '10.58.122.54',
    #  '10.58.122.51', '10.58.122.60', '10.58.122.61', '10.58.122.62', '10.58.122.63', '10.58.122.72', '10.58.122.74',
    #  '10.58.122.75', '10.58.122.87', '10.58.122.88', '10.58.122.90', '10.58.122.98', '10.58.122.96', '10.58.122.97',
    #  '10.58.122.45', '10.58.122.42', '10.58.122.46', '10.58.122.49', '10.58.122.100', '10.58.122.107', '10.58.122.109',
    #  '10.58.122.104', '10.58.122.102', '10.58.122.117', '10.58.122.206', '10.58.122.205', '10.58.122.209',
    #  '10.58.122.208', '10.58.122.41', '10.58.122.40', '10.58.122.89', '10.58.122.48', '10.58.122.53', '10.58.122.201',
    #  '10.58.122.67', '10.58.122.55', '10.58.122.47']

    # 案场：常七 -----------------------
    # IPCList =['10.58.7.52', '10.58.7.107', '10.58.7.104', '10.58.7.108', '10.58.7.54', '10.58.7.105', '10.58.7.101',
    #  '10.58.7.53', '10.58.7.102', '10.58.7.103', '10.58.7.51', '10.58.7.128', '10.58.7.126', '10.58.7.129',
    #  '10.58.7.124', '10.58.7.123', '10.58.7.125', '10.58.7.122', '10.58.7.106', '10.58.7.110', '10.58.7.117',
    #  '10.58.7.116', '10.58.7.118', '10.58.7.119', '10.58.7.121', '10.58.7.120', '10.58.7.130', '10.58.7.109',
    #  '10.58.7.127', '10.58.7.134', '10.58.7.132', '10.58.7.133', '10.58.7.131', '10.58.7.135', '10.58.7.115',
    #  '10.58.7.114', '10.58.7.113', '10.58.7.112', '10.58.7.136']

    # 案场：昆明花鹤翎 -----------------------
    # IPCList =['172.168.100.9', '172.168.100.10', '172.168.100.11', '172.168.100.100', '172.168.100.115', '172.168.100.111',
    #  '172.168.100.13']

    # 案场：遵义蔷薇国际 -----------------------
    # IPCList =['172.16.21.31', '172.16.21.32', '172.16.21.33', '172.16.21.34']

    # 案场：荆门紫薇雅著 -----------------------
    # IPCList =['10.21.249.29', '10.21.249.8', '10.21.249.3', '10.21.249.28', '10.21.249.33', '10.21.249.5', '10.21.249.31',
    #  '10.21.249.7', '10.21.249.32', '10.21.249.6', '10.21.249.2', '10.21.249.13', '10.21.249.45', '10.21.249.4',
    #  '10.21.249.37']


    # 如下所有配置信息需要按照实际情况进行配置
    IPCList = ["10.58.122.114"]  # 配置需要升级的ip
    port = '23'  # 远程访问升级设备的端口号，需要根据实际情况配置
    username = b'root\n'  # 远程访问升级设备登录的用户名，需要根据实际情况配置
    password = b'XCM#ai18G!\n'  # 远程访问升级设备登录的用户密码，需要根据实际情况配置
    finish = b'~ #'  # 远程访问升级设备的命令提示符，需要根据实际情况配置

    #nsf后台升级执行命令列表，需要根据实际情况修改具体的命令参数。
    cmds = [b'md5sum /usr/local/bin/ipcam_main;exit\r\n',
            b'reboot;exit\r\n',
            b'mount -t nfs -o nolock 10.58.150.5:/home/user/nfs /mnt/;exit\r\n',
            b'cp /mnt/XG_IPC_2020.0424_tmp3.tar /tmp/upload/;exit\r\n',
            b'md5sum /tmp/upload/XG_IPC_2020.0424_tmp3.tar;exit\r\n',
            b'cd /tmp/upload/;tar xvf XG_IPC_2020.0424_tmp3.tar;exit\r\n',
            b'killall start_app;sleep 1;killall ipcam_main;exit\r\n',
            b'/tmp/upload/patch.sh /tmp/upload/ &\r\n',
            b'pdt_get -p /dev/mtdblock7 -a;exit\r\n',
            b'ps -ef |grep ipcam_main;exit\r\n']

    # versionList = ['1.0.6.20190118','1.0.10.20190531','1.0.11.20190916','1.0.11.20190918','1.0.11.20190924','v1.0.0.20191126190700']

    #降级的版本信息
    Version1 = '1.0.10.20190531'
    version1_ipcam_main_Md5 = '40c777f9b7b7732a7c107c49d5428048'
    file1 = 'XG-IPC-1.0.10.20190531.tar'
    file1Size = os.path.getsize("../../XGTest/XG-IPC-1.0.10.20190531.tar")

    #升级的版本信息
    Version2 = '1.0.12.20200424'
    version2_ipcam_main_Md5 = '43b5e8457c09246f47cf96243a042baf'
    file2 = 'XG_IPC_2020.0424_tmp3.tar'
    file2MD5 = '6fd7a738eff231a9b960c995b696fc71'

    # 升级失败的信息记录在该文件当中
    autoUpdateFailLog = 'cameraUpdateLog0531.log'
    if os.path.exists(autoUpdateFailLog):
        os.remove(autoUpdateFailLog)

    # 不升级的摄像机文件
    upgrade_err_file = 'upgrade_err_file.log'
    if os.path.exists(upgrade_err_file):
        os.remove(upgrade_err_file)

    # for ip in IPCList:
    #     p1 = Process(target=run, args=(ip,))
    #     p1.start()
    run(IPCList[0])





