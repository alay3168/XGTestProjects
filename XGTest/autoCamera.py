import json
import sys
import time

from websocket import create_connection


# 登录
def Login(ws):
    login_req = """{"Method":"Login","Page":"Login","Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}"""
    ws.send(login_req)  ##发送消息
    result = ws.recv()  ##接收消息
    result = json.loads(result)
    if result["RetCode"] == 0:
        print("登录成功")
    else:
        print("登录失败")
        sys.exit()


# 退出
def Logout(ws):
    logout_req = """{"Method":"Logout","Page":"Logout"}"""
    ws.send(logout_req)  ##发送消息
    result = ws.recv()  ##接收消息
    result = json.loads(result)
    if result["RetCode"] == 0:
        print("退出成功")
    else:
        print("退出失败")
        sys.exit()


if __name__ == "__main__":
    cameraIP = "ws://10.58.122.115:8000"
    ws = create_connection(cameraIP)
    num = 0
    while True:
        Login(ws)
        time.sleep(1)
        Logout(ws)
        print("执行多少次：%d" % (num))
        num += 1
