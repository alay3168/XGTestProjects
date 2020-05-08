import json
import logging
import os
import random
import telnetlib
import threading
import time
import traceback
from datetime import datetime

from websocket import create_connection


# 登录接口请求函数
def Login(boxIP, ws, number):
    print(str(
        datetime.now()) + "：——————————————————————————————%s开始执行第：%d次升级——————————————————————————————" % (
              boxIP, number))
    login_req = """{"Method":"Login","Page":"Login","Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}"""
    while True:
        ws.send(login_req)  ##发送消息
        result = ws.recv()  ##接收消息
        result = json.loads(result)
        if result["RetCode"] == 0:
            print(str(datetime.now()) + "：%s盒子执行Login接口登录成功" % boxIP)
            break
        else:
            errorMessage = str(datetime.now()) + "：第%d次升级，%s盒子执行Login接口登录失败返回信息：%s" % (number, boxIP, result)
            print(errorMessage)
            with open(autoUpdateFailLog, 'a') as f:
                f.write(errorMessage)
                f.write('\n')
            time.sleep(5)


# 获取设备版本信息接口请求函数
def GetConfig(boxIP, ws, number):
    device_req = """{"Method" : "GetConfig","Page" : "DevInfo"}"""
    ws.send(device_req)  ##发送消息
    device_res = ws.recv()  ##接收消息#
    DevFWstr = json.loads(device_res)
    RetCode = DevFWstr["RetCode"]
    if RetCode != 0:
        errorMessage = str(datetime.now()) + "：第%d次升级，%s盒子执行GetConfig接口获取版本信息失败，其返回信息为：%s" % (number, boxIP, DevFWstr)
        print(errorMessage)
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')
    else:
        print(str(datetime.now()) + "：%s盒子执行GetConfig接口获取设备版本信息成功" % boxIP)
        DevFW = json.loads(DevFWstr["Message"])["Device-Properties"]["DevFW"]
        return DevFW


# 执行开始升级接口请求函数
def UpgradeStar(boxIP, ws, filename, tolalSize, number):
    starUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                     "Message": {"Status": "Start", "File": "XG-IPC-1.0.10.20190531.tar", "TotalSize": 15011840,
                                 "PackSize": 5120000}}
    starUpdateReq["Message"]["File"] = filename
    starUpdateReq["Message"]["TotalSize"] = tolalSize
    starUpdateReqJosn = json.dumps(starUpdateReq)
    ws.send(starUpdateReqJosn)  ##发送消息
    starUpdateRes = ws.recv()  ##接收消息#
    starUpdateRes = json.loads(starUpdateRes)
    RetCode = starUpdateRes["RetCode"]
    if RetCode != 0:
        errorMessage = str(datetime.now()) + "：第%d次升级，%s盒子执行star接口开始传输升级包失败，其返回信息：%s，执行getlog.sh备份盒子升级日志" % (
            number, boxIP, starUpdateRes)
        print(errorMessage)
        cmd_res(boxIP, port, username, password, finish, cmds[2])
        cmd_res(boxIP, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')
        # 发送transFinish清空盒子升级状态
        transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                                "Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
        transFinishUpdateReq["Message"]["File"] = filename
        transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
        ws.send(transFinishUpdateReqJosn)
        return
    print(str(datetime.now()) + "：%s盒子执行star接口开始传输升级包成功" % boxIP)


# 传输升级包接口请求函数
def UpgradeTrans(boxIP, ws, num, file, filename, endNum, number):
    PackNum = 1
    transUpdate = {"Method": "Maintain", "Page": "Upgrade",
                   "Message": {"Status": "Trans", "File": "XG-IPC-1.0.10.20190531.tar", "CurSize": 5120000,
                               "PackNum": 1}}
    print(str(datetime.now()) + "：%s盒子执行Trans接口开始发送升级包文件" % boxIP)
    while True:
        buf = file.read(5120000)
        if num:
            transUpdate["Message"]["File"] = filename
            transUpdate["Message"]["PackNum"] = PackNum
            transUpdateReqJosn = json.dumps(transUpdate)
            transUpdateReq = bytes(transUpdateReqJosn, encoding='utf8') + bytes('\0', encoding='utf8') + buf
            ws.send(transUpdateReq)
            print("-", end='')
            transUpdateReqRes = ws.recv()
            PackNum += 1
            num -= 1
        else:
            print("")
            print(str(datetime.now()) + "：%s盒子传输最后一个升级包文件%d：" % (boxIP, PackNum))
            transUpdate["Message"]["File"] = filename
            transUpdate["Message"]["PackNum"] = PackNum
            transUpdate["Message"]["CurSize"] = endNum
            transUpdateReqJosn = json.dumps(transUpdate)
            transUpdateReqEnd = bytes(transUpdateReqJosn, encoding='utf8') + bytes('\0', encoding='utf8') + buf
            ws.send(transUpdateReqEnd)
            transUpdateReqEndRes = ws.recv()
            RetCode = json.loads(transUpdateReqEndRes)["RetCode"]
            if RetCode != 0:
                errorMessage = str(datetime.now()) + "：第%d次升级，%s盒子执行Trans接口传输文件失败,其返回信息：%s，执行getlog.sh备份盒子升级日志" % (
                    number, boxIP, transUpdateReqEndRes)
                print(errorMessage)
                cmd_res(boxIP, port, username, password, finish, cmds[2])
                cmd_res(boxIP, port, username, password, finish, cmds[4])
                with open(autoUpdateFailLog, 'a') as f:
                    f.write(errorMessage)
                    f.write('\n')
                # 发送transFinish清空盒子升级状态
                transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                                        "Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
                transFinishUpdateReq["Message"]["File"] = filename
                transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
                ws.send(transFinishUpdateReqJosn)
                return
            break
    print(str(datetime.now()) + "：%s盒子执行Trans接口传输升级包文件完成" % boxIP)


# 发送传输文件完成却接口请求函数
def UpgradeTransFinish(boxIP, ws, filename, number):
    transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                            "Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
    transFinishUpdateReq["Message"]["File"] = filename
    transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
    ws.send(transFinishUpdateReqJosn)
    starUpdateRes = ws.recv()
    starUpdateRes = json.loads(starUpdateRes)
    if starUpdateRes["RetCode"] is 0:
        print(str(datetime.now()) + "：%s盒子执行TransFinish接口确认传输完整升级包文件成功" % boxIP)
    else:
        errorMessage = str(datetime.now()) + "：第%d次升级，%s盒子执行TransFinish接口确认传输完整升级包文件失败,其返回信息：%s，执行getlog.sh备份盒子升级日志" % (
            number, boxIP, starUpdateRes)
        print(errorMessage)
        cmd_res(boxIP, port, username, password, finish, cmds[2])
        cmd_res(boxIP, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')
        # print(str(datetime.now())+"：第%d次升级，执行TransFinish接口确认传输完整升级包文件成功,其返回信息：%s"%(number,starUpdateRes))


# 开始传输文件执行升级
def Upgrade(boxIP, ws, filename, fileSize, number):
    file = open(filename, mode='rb')
    Num = fileSize // 5120000
    endNum = fileSize % 5120000
    UpgradeStar(boxIP, ws, filename, fileSize, number)
    UpgradeTrans(boxIP, ws, Num, file, filename, endNum, number)
    UpgradeTransFinish(boxIP, ws, filename, number)
    time.sleep(300)


def cmd_res(boxIP, port, username, password, finish, cmd):
    while True:
        try:
            tn = telnetlib.Telnet(boxIP, port=port, timeout=10)
            print(str(datetime.now()) + "：尝试telnet登录%s盒子" % boxIP)
        except Exception as e:
            print(str(datetime.now()) + "：尝试telnet登录%s盒子失败：%s" % (boxIP, e))
            traceback.print_exc(file=open(autoUpdateFailLog, 'a'))
            continue
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
            break
    return Outres


# 升级完成后获取升级文件的MD5值
def get_md5(boxIP, port, username, password, finish, cmds):
    while True:
        Outres = cmd_res(boxIP, port, username, password, finish, cmds[0])
        Outres = str(Outres, encoding="utf-8")
        print("检测%s盒子 BoxMain进程结果:%s" % (boxIP, Outres))
        if '/usr/local/app/bin/BoxMain' in Outres:
            time.sleep(5)
            getmd5res = cmd_res(boxIP, port, username, password, finish, cmds[1])
            BoxMainMD5 = str(getmd5res, encoding="utf8").split("\r\n")[7].split("=")[1]
            BoxMaindebugMD5 = str(getmd5res, encoding="utf8").split("\r\n")[8].split("=")[1]
            wwwMD5 = str(getmd5res, encoding="utf8").split("\r\n")[9].split("=")[1]
            print(str(datetime.now()) + "：检测%s盒子 BoxMain主进程已经正常启动，获取MD5值" % boxIP)
            print("BoxMainMD5:%s" % BoxMainMD5)
            print("BoxMaindebugMD5:%s" % BoxMaindebugMD5)
            print("wwwMD5:%s" % wwwMD5)
            break
        else:
            print(str(datetime.now()) + "：检测%s盒子 BoxMain主进程没有正常启动，休眠5s钟继续确认BoxMain" % boxIP)
            time.sleep(5)
            continue

    return (BoxMainMD5, BoxMaindebugMD5, wwwMD5)


def Upg_to_confirm(boxIP, BoxMainMD5, BoxMaindebugMD5, wwwMD5, number):
    BMMD5, BMDMD5, wMD5 = get_md5(boxIP, port, username, password, finish, cmds)
    if BoxMainMD5 == BMMD5 and BoxMaindebugMD5 == BMDMD5 and wwwMD5 == wMD5:
        print("%s盒子升级成功" % boxIP)
    else:
        errorMessage = str(
            datetime.now()) + "：——————————————————————————————第：%d次升级，%s盒子执行MD5校验失败,执行getlog.sh保存日志至/usr/local/stor/logbak——————————————————————————————" % (
                           number, boxIP)
        print(errorMessage)
        # print(str(datetime.now()) +"：———————————————————————————————第：%d次升级，执行MD5校验失败,执行getlog.sh保存日志至/usr/local/stor/logbak———————————————————" % number)
        cmd_res(boxIP, port, username, password, finish, cmds[2])
        cmd_res(boxIP, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')


def run(boxIP):
    number = 1
    while number <= 10000:
        try:
            ws = create_connection(websocketIP, timeout=60)
            Login(boxIP, ws, number)
            DevFW = GetConfig(boxIP, ws, number)
            all_index = set(range(len(updateFileList)))
            j = [i for i in range(len(updateFileList)) if DevFW == updateFileList[i][0]]
            if not j:
                j = all_index  # 0
            else:
                j = all_index - set([j[0]])  # (j[0] + 1) % len(updateFileList)
            j = random.choice(list(j))
            print(str(datetime.now()) + "：%s盒子开始执行%s版本升级" % (boxIP, updateFileList[j][0]))
            Upgrade(boxIP, ws, updateFileList[j][1], updateFileList[j][2], number)
            Upg_to_confirm(boxIP, updateFileList[j][3], updateFileList[j][4], updateFileList[j][5], number)
            endTime = datetime.now()
            print("%s盒子本次升级共耗时:%s" % (boxIP, str(endTime - startTime)))
            print(str(
                endTime) + "：——————————————————————————————%s盒子升级MD5校验成功，第：%d次升级成功——————————————————————————————" % (
                      boxIP, number))
            number += 1
        except Exception as e:
            errorMessage = str(datetime.now()) + "：%s盒子第%d次升级出现异常执行getlog.sh保存日志至/usr/local/stor/logbak，:%s，" % (
                boxIP, number, e)
            print(errorMessage)
            with open(autoUpdateFailLog, 'a') as f:
                f.write('\n')
                f.write(errorMessage)
                f.write('\n')
            traceback.print_exc(file=open(autoUpdateFailLog, 'a'))
            cmd_res(boxIP, port, username, password, finish, cmds[2])
            cmd_res(boxIP, port, username, password, finish, cmds[4])
            ws.close()
            time.sleep(300)
            number += 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')

    # 如下配置信息需要按照实际情况进行配置
    boxIPList = ["10.58.122.108"]  # 配置需要升级的boxIP
    port = '23'  # 远程访问升级设备的端口号，需要根据实际情况配置
    username = b'root\n'  # 远程访问升级设备登录的用户名，需要根据实际情况配置
    password = b'HZ*SF#ai1xS!\n'  # 远程访问升级设备登录的用户密码，需要根据实际情况配置
    finish = b'~ #'  # 远程访问升级设备的命令提示符，需要根据实际情况配置
    cmds = [b'ps -ef |grep BoxMain;exit\n', b'cat /usr/local/app/bin/app_info.txt;exit\n', b'getlog.sh;exit\n',
            b'mkdir /usr/local/stor/logbak;exit\n', b'cp /usr/local/stor/*.* /usr/local/stor/logbak/;exit\n']

    autoUpdateFailLog = 'autoUpdateFailLog.txt'  # 升级失败的信息记录在改文件当中
    if os.path.exists(autoUpdateFailLog):
        os.remove(autoUpdateFailLog)

    updateFileList = [
        ["v1.0.0.20200117152700", "xgai1527a.bin", os.path.getsize("xgai1527a.bin"), "9de9117487c27fa4f395d33e929e9d2f",
         "6e607944ee2a46a6e4fa73fd7ca1f83b", "f081f94a3dcca313baaaada47607f6cf"],
        ["v1.0.0.20200117153200", "xgai1532d.bin", os.path.getsize("xgai1532d.bin"), "3b3fb09556a6a37b35066128889c490f",
         "48cc1a9b3d63af88098450a9d2049763", "aa8fd705de944184e53a21c0640aac7a"]]

    for boxIP in boxIPList:
        websocketIP = "ws://" + boxIP + ":8000"
        cmd_res(boxIP, port, username, password, finish, cmds[3])
        startTime = datetime.now()
        try:
            boxIP = threading.Thread(target=run, args=(boxIP,))
            boxIP.start()
        except Exception as e:
            print(boxIP, ":启动升级线程失败%s" % e)
            traceback.print_exc(file=open(autoUpdateFailLog, 'a'))
