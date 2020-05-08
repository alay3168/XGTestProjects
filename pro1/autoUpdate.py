from websocket import create_connection
import json
import os
import time
from datetime import datetime
import sys
import telnetlib

#登录接口请求函数
def Login (websocketIP,ws):
    ws = ws
    login_req = """{"Method":"Login","Page":"Login","Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}"""
    ws.send(login_req)  ##发送消息
    result = ws.recv()  ##接收消息
    result = json.loads(result)
    if result["RetCode"] == 0:
        print(str(datetime.now())+"：执行Login接口登录成功")
    else:
        errorMessage = str(datetime.now())+"：第%d次升级，执行Login接口登录失败返回信息：%s"%(number,result)
        print(errorMessage)
        with open(autoUpdateFailLog,'a') as f:
            f.write(errorMessage)
            f.write('\n')
        return


#获取设备版本信息接口请求函数
def GetConfig(ws):
    ws =ws
    device_req = """{"Method" : "GetConfig","Page" : "DevInfo"}"""
    ws.send(device_req)  ##发送消息
    device_res = ws.recv()  ##接收消息#
    DevFWstr = json.loads(device_res)
    RetCode =DevFWstr["RetCode"]
    if RetCode !=0:
        errorMessage = str(datetime.now())+"：第%d次升级，执行GetConfig接口获取版本信息失败，其返回信息为：%s"%(number,DevFWstr)
        print(errorMessage)
        with open(autoUpdateFailLog,'a') as f:
            f.write(errorMessage)
            f.write('\n')
        return
    else:
        print(str(datetime.now())+"：执行GetConfig接口获取设备版本信息成功")
        DevFW = json.loads(DevFWstr["Message"])["Device-Properties"]["DevFW"]
        return DevFW

#执行开始升级接口请求函数
def UpgradeStar(filename,tolalSize,ws):
    ws=ws
    starUpdateReq = {"Method":"Maintain","Page":"Upgrade","Message":{"Status":"Start","File":"XG-IPC-1.0.10.20190531.tar","TotalSize":15011840,"PackSize":5120000}}
    starUpdateReq["Message"]["File"] = filename
    starUpdateReq["Message"]["TotalSize"]=tolalSize
    starUpdateReqJosn = json.dumps(starUpdateReq)
    ws.send(starUpdateReqJosn)##发送消息
    starUpdateRes = ws.recv()##接收消息#
    starUpdateRes = json.loads(starUpdateRes)
    RetCode = starUpdateRes["RetCode"]
    if RetCode !=0:
        errorMessage = str(datetime.now())+"：第%d次升级，执行star接口开始传输升级包失败，其返回信息：%s，执行getlog.sh备份盒子升级日志"%(number,starUpdateRes)
        print(errorMessage)
        cmd_res(deviceIP, port, username, password, finish, cmds[2])
        cmd_res(deviceIP, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog,'a') as f:
            f.write(errorMessage)
            f.write('\n')
        #发送transFinish清空盒子升级状态
        transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade",
                                "Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
        transFinishUpdateReq["Message"]["File"] = filename
        transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
        ws.send(transFinishUpdateReqJosn)
        return
    print(str(datetime.now())+"：执行star接口开始传输升级包成功")


#传输升级包接口请求函数
def UpgradeTrans(num,file,filename,endNum,ws):
    ws =ws
    PackNum =1
    num =num
    file = file
    filename = filename
    endNum = endNum
    transUpdate = {"Method":"Maintain","Page":"Upgrade","Message":{"Status":"Trans","File":"XG-IPC-1.0.10.20190531.tar","CurSize":5120000,"PackNum":1}}
    print(str(datetime.now()) + "：执行Trans接口开始发送升级包文件")
    while True:
        buf = file.read(5120000)
        if num:
            transUpdate["Message"]["File"] = filename
            transUpdate["Message"]["PackNum"]=PackNum
            transUpdateReqJosn = json.dumps(transUpdate)
            transUpdateReq = bytes(transUpdateReqJosn,encoding='utf8') + bytes('\0', encoding='utf8') + buf
            ws.send(transUpdateReq)
            print("-",end='')
            transUpdateReqRes = ws.recv()
            PackNum += 1
            num -=1
        else:
            print("")
            print(str(datetime.now()) + "：传输最后一个升级包文件：",PackNum)
            transUpdate["Message"]["File"] = filename
            transUpdate["Message"]["PackNum"] = PackNum
            transUpdate["Message"]["CurSize"] = endNum
            transUpdateReqJosn = json.dumps(transUpdate)
            transUpdateReqEnd = bytes(transUpdateReqJosn, encoding='utf8') + bytes('\0', encoding='utf8') + buf
            ws.send(transUpdateReqEnd)
            transUpdateReqEndRes = ws.recv()
            RetCode = json.loads(transUpdateReqEndRes)["RetCode"]
            if RetCode !=0:
                errorMessage = str(datetime.now()) + "：第%d次升级，执行Trans接口传输文件失败,其返回信息：%s，执行getlog.sh备份盒子升级日志"%(number,transUpdateReqEndRes)
                print(errorMessage)
                cmd_res(deviceIP, port, username, password, finish, cmds[2])
                cmd_res(deviceIP, port, username, password, finish, cmds[4])
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
    print(str(datetime.now())+"：执行Trans接口传输升级包文件完成")

#发送传输文件完成却接口请求函数
def UpgradeTransFinish(filename,ws):
    ws = ws
    transFinishUpdateReq = {"Method": "Maintain", "Page": "Upgrade","Message": {"Status": "TransFinish", "File": "XG-IPC-1.0.10.20190531.tar"}}
    transFinishUpdateReq["Message"]["File"] = filename
    transFinishUpdateReqJosn = json.dumps(transFinishUpdateReq)
    ws.send(transFinishUpdateReqJosn)
    starUpdateRes = ws.recv()
    # print("TransFinish接口请求发送成功，等待返回！！！！")
    # try:
    #     starUpdateRes = ws.recv()
    # except Exception as e:
    #     print(str(datetime.now()) + "：执行TransFinish接口确认传输完整升级包文件失败,直接终止该接口函数执行，执行下一次升级操作:%s"%e)
    #     return
    # print("TransFinish接口返回成功！！！")
    starUpdateRes = json.loads(starUpdateRes)
    if starUpdateRes["RetCode"] is 0:
        print(str(datetime.now())+"：执行TransFinish接口确认传输完整升级包文件成功")
    else:
        errorMessage = str(datetime.now()) + "：第%d次升级，执行TransFinish接口确认传输完整升级包文件失败,其返回信息：%s，执行getlog.sh备份盒子升级日志"%(number,starUpdateRes)
        print(errorMessage)
        cmd_res(deviceIP, port, username, password, finish, cmds[2])
        cmd_res(deviceIP, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')
        #print(str(datetime.now())+"：第%d次升级，执行TransFinish接口确认传输完整升级包文件成功,其返回信息：%s"%(number,starUpdateRes))
        return


#开始传输文件执行升级
def Upgrade(filename,fileSize,ws):
    file = open(filename, mode='rb')
    Num = fileSize // 5120000
    endNum = fileSize % 5120000
    UpgradeStar(filename, fileSize, ws)
    UpgradeTrans(Num, file, filename, endNum, ws)
    UpgradeTransFinish(filename, ws)
    time.sleep(300)

def cmd_res(deviceIP, port,username, password, finish, cmd):
    while True:
        try:
            tn = telnetlib.Telnet(deviceIP, port=port, timeout=10)
            print(str(datetime.now())+"：尝试telnet登录盒子")
        except Exception as e:
            print( str(datetime.now())+"：尝试telnet登录盒子失败：%s"%e)
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


#升级完成后获取升级文件的MD5值
def get_md5(deviceIP, port,username, password, finish, cmds):
    while True:
        Outres = cmd_res(deviceIP, port,username, password, finish, cmds[0])
        Outres=str(Outres, encoding="utf-8")
        print("检测BoxMain进程结果:%s"%Outres)
        if '/usr/local/app/bin/BoxMain' in Outres:
            time.sleep(5)
            getmd5res = cmd_res(deviceIP, port, username, password, finish, cmds[1])
            BoxMainMD5 = str(getmd5res, encoding="utf8").split("\r\n")[7].split("=")[1]
            BoxMaindebugMD5 = str(getmd5res, encoding="utf8").split("\r\n")[8].split("=")[1]
            wwwMD5 = str(getmd5res, encoding="utf8").split("\r\n")[9].split("=")[1]
            print(str(datetime.now()) + "：检测BoxMain主进程已经正常启动，获取MD5值")
            print("BoxMainMD5:%s" % BoxMainMD5)
            print("BoxMaindebugMD5:%s" % BoxMaindebugMD5)
            print("wwwMD5:%s" % wwwMD5)
            break
        else:
            print(str(datetime.now()) + "：检测BoxMain主进程没有正常启动，休眠5s钟继续确认BoxMain")
            time.sleep(5)
            continue

    return (BoxMainMD5, BoxMaindebugMD5, wwwMD5)

def Upg_to_confirm(BoxMainMD5,BoxMaindebugMD5,wwwMD5):
    BMMD5, BMDMD5, wMD5 = get_md5(deviceIP, port, username, password, finish, cmds)
    if BoxMainMD5 == BMMD5 and BoxMaindebugMD5 == BMDMD5 and wwwMD5 == wMD5:
        print("升级成功")
    else:
        errorMessage = str(datetime.now()) + "：———————————————————————————————第：%d次升级，执行MD5校验失败,执行getlog.sh保存日志至/usr/local/stor/logbak———————————————————" % number
        print(errorMessage)
        #print(str(datetime.now()) +"：———————————————————————————————第：%d次升级，执行MD5校验失败,执行getlog.sh保存日志至/usr/local/stor/logbak———————————————————" % number)
        cmd_res(deviceIP, port, username, password, finish, cmds[2])
        cmd_res(deviceIP, port, username, password, finish, cmds[4])
        with open(autoUpdateFailLog, 'a') as f:
            f.write(errorMessage)
            f.write('\n')

if __name__ == "__main__":
    #如下配置信息需要按照实际情况进行配置
    deviceIP = "10.58.122.237"
    port = '23'  # 远程访问升级设备的端口号，需要根据实际情况配置
    username = b'root\n'  # 远程访问升级设备登录的用户名，需要根据实际情况配置
    password = b'HZ*SF#ai1xS!\n'  # 远程访问升级设备登录的用户密码，需要根据实际情况配置
    finish = b'~ #'  # 远程访问升级设备的命令提示符，需要根据实际情况配置
    cmds = [b'ps -ef |grep BoxMain;exit\n', b'cat /usr/local/app/bin/app_info.txt;exit\n', b'getlog.sh;exit\n',b'mkdir /usr/local/stor/logbak;exit\n',b'cp /usr/local/stor/*.* /usr/local/stor/logbak/;exit\n']
    cmd_res(deviceIP, port, username, password, finish, cmds[3])

    autoUpdateFailLog= 'autoUpdateFailLog.txt'#升级失败的信息记录在改文件当中

    websocketIP = "ws://"+ deviceIP+":8000"#web与升级设备的websocket连接地址

    Version1 = "v1.0.0.20200117152700"#升级文件1的版本号，需要根据实际情况配置
    Version2 = "v1.0.0.20200117153200"#升级文件2的版本号，需要根据实际情况配置

    fileName1 = "xgai1527.bin"#升级文件1的文件名，需要根据实际情况配置
    fileName2 = "xgai1532.bin"#升级文件2的文件名，需要根据实际情况配置

    fileSize1 = os.path.getsize("xgai1527.bin")#升级文件1的大小，需要根据实际情况配置
    fileSize2 = os.path.getsize("xgai1532.bin")#升级文件2的大小，需要根据实际情况配置

    BoxMainMD51 = "9de9117487c27fa4f395d33e929e9d2f"  # 升级文件1的BoxMain的MD5值，需要根据实际情况配置
    BoxMaindebugMD51 = "6e607944ee2a46a6e4fa73fd7ca1f83b"  # 升级文件1的BoxMaindebug的MD5值，需要根据实际情况配置
    wwwMD51 = "f081f94a3dcca313baaaada47607f6cf"  # 升级文件1的wwwMD51的MD5值，需要根据实际情况配置

    BoxMainMD52 = "3b3fb09556a6a37b35066128889c490f"  # 升级文件2的BoxMain的MD5值，需要根据实际情况配置
    BoxMaindebugMD52 = "48cc1a9b3d63af88098450a9d2049763"  # 升级文件2的BoxMaindebug的MD5值，需要根据实际情况配置
    wwwMD52 = "aa8fd705de944184e53a21c0640aac7a"  # 升级文件2的wwwMD51的MD5值，需要根据实际情况配置

    number = 1
    retry = 1
    startTime = datetime.now()
    while number<=10000:
        if retry>6 :
            print("累计重试升级5次均异常，终止升级")
            sys.exit()
        try:
            print(str(startTime) + "：——————————————————————————————开始执行第：%d次升级—————————————————————————————" % number)
            ws = create_connection(websocketIP,timeout=60)
            Login(websocketIP,ws)
            DevFW = GetConfig(ws)
            if DevFW == Version1:
                print(str(datetime.now())+"：开始执行Version2升级")
                Upgrade(fileName2,fileSize2,ws)
                Upg_to_confirm(BoxMainMD52,BoxMaindebugMD52,wwwMD52)
                endTime = datetime.now()
                print("本次升级共耗时:%s" % str(endTime - startTime))
                print(str(endTime) + "：——————————————————————————————MD5校验成功，第：%d次升级成功————————————————" % number)
                number += 1
            else:
                print(str(datetime.now())+"：开始执行Version1升级")
                Upgrade(fileName1,fileSize1,ws)
                Upg_to_confirm(BoxMainMD51,BoxMaindebugMD51,wwwMD51)
                endTime = datetime.now()
                print("本次升级共耗时:%s" % str(endTime - startTime))
                print(str(endTime) + "：——————————————————————————————MD5校验成功，第：%d次升级成功————————————————" % number)
                number += 1
        except Exception as e:
                #print(str(datetime.now())+"：第%d升级出现异常执行getlog.sh保存日志至/usr/local/stor/logbak，:%s，"%(number,e))
            errorMessage = str(datetime.now())+"：第%d升级出现异常执行getlog.sh保存日志至/usr/local/stor/logbak，:%s，"%(number,e)
            print(errorMessage)
            with open(autoUpdateFailLog, 'a') as f:
                f.write(errorMessage)
                f.write('\n')
            getlogres = cmd_res(deviceIP, port, username, password, finish, cmds[2])
            cmd_res(deviceIP, port, username, password, finish, cmds[4])
            time.sleep(300)
            retry += 1
            number += 1