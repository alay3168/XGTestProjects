from websocket import create_connection
import json
import os
import time
from datetime import datetime
import telnetlib
import threading
import logging
import traceback
import random


# 登录接口请求函数
def Login(boxIP, ws, number):
    login_req = """{"Method":"Login","Page":"Login","Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}"""
    while True:
        print(str(datetime.now()) + "执行Login登录请求消息：", login_req)
        ws.send(login_req)  ##发送消息
        result = ws.recv()  ##接收消息
        result = json.loads(result)
        print(str(datetime.now()) + "执行Login登录返回消息：", result)
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
    print(str(datetime.now()) + "执行GetConfig获取版本信息请求消息：", device_req)
    ws.send(device_req)  ##发送消息
    device_res = ws.recv()  ##接收消息#
    DevFWstr = json.loads(device_res)
    print(str(datetime.now()) + "执行GetConfig获取版本信息返回消息：", DevFWstr)
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
    print(str(datetime.now()) + "执行UpgradeStar开始升级接口请求消息：", starUpdateReqJosn)
    ws.send(starUpdateReqJosn)  ##发送消息
    starUpdateRes = ws.recv()  ##接收消息#
    starUpdateRes = json.loads(starUpdateRes)
    print(str(datetime.now()) + "执行UpgradeStar开始升级接口返回消息：", starUpdateRes)
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
            #print(str(datetime.now()) + "执行UpgradeTrans传输升级包请求消息%d：%s" % (PackNum, transUpdateReq))
            ws.send(transUpdateReq)
            print("-", end='')
            transUpdateReqRes = ws.recv()
            #print(str(datetime.now()) + "执行UpgradeTrans传输升级包响应消息%d：%s" % (PackNum, transUpdateReqRes))
            print()
            PackNum += 1
            num -= 1
        else:
            #print(str(datetime.now()) + "：%s盒子传输最后一个升级包文件%d：" % (boxIP, PackNum))
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
    print(str(datetime.now()) + "执行UpgradeTransFinish发送传输文件完成接口请求消息%s" % transFinishUpdateReqJosn)
    ws.send(transFinishUpdateReqJosn)
    starUpdateRes = ws.recv()
    starUpdateRes = json.loads(starUpdateRes)
    print(str(datetime.now()) + "执行UpgradeTransFinish发送传输文件完成接口响应消息%s" % starUpdateRes)
    if starUpdateRes["RetCode"] == 0:
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
            tn.close()
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
    indx1 = range(len(version1FileList))
    indx2 = range(len(version2FileList))
    while number <= 10000:
        # j = random.choice(list(indx))
        try:
            ws = create_connection(websocketIP, timeout=60)
            Login(boxIP, ws, number)
            DevFW = GetConfig(boxIP, ws, number)
            if version1 == DevFW:
                j = random.choice(list(indx2))
                print(str(
                    datetime.now()) + "：——————————————————————————————%s盒子开始执行第：%d次升级，升级的版本是%s,升级的文件包是%s——————————————————————————————" % (
                          boxIP, number, version2, version2FileList[j][0]))
                Upgrade(boxIP, ws, version2FileList[j][0], version2FileList[j][1], number)
                Upg_to_confirm(boxIP, version2FileList[j][2], version2FileList[j][3], version2FileList[j][4], number)
                endTime = datetime.now()
                print("%s盒子执行%s版本%s文件包进行升级共耗时:%s" % (boxIP, version2, version2FileList[j][0], str(endTime - startTime)))
                print(str(
                    endTime) + "：——————————————————————————————%s盒子执行%s版本%s文件包升级MD5校验成功，第：%d次升级成功——————————————————————————————" % (
                      boxIP, version2, version2FileList[j][0], number))
                number += 1
                ws.close()
            else:
                j = random.choice(list(indx1))
                print(str(
                    datetime.now()) + "：——————————————————————————————%s盒子开始执行第：%d次升级，升级的版本是%s,升级的文件包是%s——————————————————————————————" % (
                          boxIP, number, version1, version1FileList[j][0]))
                Upgrade(boxIP, ws, version1FileList[j][0], version1FileList[j][1], number)
                Upg_to_confirm(boxIP, version1FileList[j][2], version1FileList[j][3], version1FileList[j][4], number)
                endTime = datetime.now()
                print("%s盒子执行%s版本%s文件包进行升级共耗时:%s" % (boxIP, version1, version1FileList[j][0], str(endTime - startTime)))
                print(str(
                    endTime) + "：——————————————————————————————%s盒子执行%s版本%s文件包升级MD5校验成功，第：%d次升级成功——————————————————————————————" % (
                      boxIP, version1, version1FileList[j][0], number))
                number += 1
                ws.close()
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
    boxIPList = ["10.58.122.201"]  # 配置需要升级的boxIP
    port = '23'  # 远程访问升级设备的端口号，需要根据实际情况配置
    username = b'root\n'  # 远程访问升级设备登录的用户名，需要根据实际情况配置
    password = b'HZ*SF#ai1xS!\n'  # 远程访问升级设备登录的用户密码，需要根据实际情况配置
    finish = b'~ #'  # 远程访问升级设备的命令提示符，需要根据实际情况配置
    cmds = [b'ps -ef |grep BoxMain;exit\n', b'cat /usr/local/app/bin/app_info.txt;exit\n', b'getlog.sh;exit\n',
            b'mkdir /usr/local/stor/logbak;exit\n', b'cp /usr/local/stor/*.* /usr/local/stor/logbak/;exit\n']

    autoUpdateFailLog = 'mulBoxRandomAutoUpdateLog.txt'  # 升级失败的信息记录在该文件当中
    if os.path.exists(autoUpdateFailLog):
        os.remove(autoUpdateFailLog)

    version1 = "v1.0.0.20200310143200"
    version1FileList = [["xgaia1.bin", os.path.getsize("xgaia1.bin"), "d51f68d6ab6e7915c910ccf8b71f7584",
                         "6365d2c2306d800942d050e9df7759ee", "93fe2fcad38a1886dd811630fde2497d"],
                        ["xgaib1.bin", os.path.getsize("xgaib1.bin"), "d51f68d6ab6e7915c910ccf8b71f7584",
                         "6365d2c2306d800942d050e9df7759ee", "93fe2fcad38a1886dd811630fde2497d"],
                        ["xgaic1.bin", os.path.getsize("xgaic1.bin"), "d51f68d6ab6e7915c910ccf8b71f7584",
                         "6365d2c2306d800942d050e9df7759ee", "93fe2fcad38a1886dd811630fde2497d"],
                        ["xgaid1.bin", os.path.getsize("xgaid1.bin"), "d51f68d6ab6e7915c910ccf8b71f7584",
                         "6365d2c2306d800942d050e9df7759ee", "93fe2fcad38a1886dd811630fde2497d"],
                        ["xgaie1.bin", os.path.getsize("xgaie1.bin"), "d51f68d6ab6e7915c910ccf8b71f7584",
                         "6365d2c2306d800942d050e9df7759ee", "93fe2fcad38a1886dd811630fde2497d"]]

    version2 = "v1.0.0.20200310142700"
    version2FileList = [["xgaia2.bin", os.path.getsize("xgaia2.bin"), "5547264c5113187d0d66eaef0e80c9d4",
                         "e299077848f7bb7fa318b3d943765d1d", "f7a1f5d6553332cfccc262c1535a2f2d"],
                        ["xgaib2.bin", os.path.getsize("xgaib2.bin"), "5547264c5113187d0d66eaef0e80c9d4",
                         "e299077848f7bb7fa318b3d943765d1d", "f7a1f5d6553332cfccc262c1535a2f2d"],
                        ["xgaic2.bin", os.path.getsize("xgaic2.bin"), "5547264c5113187d0d66eaef0e80c9d4",
                         "e299077848f7bb7fa318b3d943765d1d", "f7a1f5d6553332cfccc262c1535a2f2d"],
                        ["xgaid2.bin", os.path.getsize("xgaid2.bin"), "5547264c5113187d0d66eaef0e80c9d4",
                         "e299077848f7bb7fa318b3d943765d1d", "f7a1f5d6553332cfccc262c1535a2f2d"],
                        ["xgaie2.bin", os.path.getsize("xgaie2.bin"), "5547264c5113187d0d66eaef0e80c9d4",
                         "e299077848f7bb7fa318b3d943765d1d", "f7a1f5d6553332cfccc262c1535a2f2d"]]

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