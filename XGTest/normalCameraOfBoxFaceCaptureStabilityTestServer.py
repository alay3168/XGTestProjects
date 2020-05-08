import itertools
import json
import logging
import os
import shutil
import sys
import time
import traceback
from datetime import datetime
import socket
import requests
from influxdb import InfluxDBClient
from websocket import create_connection


def sokcetServer(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, 6666))  # 在同一台主机的ip下使用测试ip进行通信
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Wait for Connection..................")
    return s

#登录盒子
def Login (ws):
    login_req = """{"Method":"Login","Page":"Login","Message":{"Login-Properties":{"UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}"""
    ws.send(login_req)  ##发送消息
    result = ws.recv()  ##接收消息
    result = json.loads(result)
    if result["RetCode"] == 0:
        print(str(datetime.now())+"：登录盒子web管理界面成功")
    else:
        print(str(datetime.now())+"：登录盒子web管理界面失败：%s"%result)
        sys.exit()

#为盒子添加视频流
def addRtspStream(ws,rtspAddr,indx):
    addRtspStream_req = {"Method":"SetConfig","Page":"ChnInfo","Message":{"ChnInfo-Properties":{"OpType":0,"RegisterTime":"2020-01-10 15:37:02","DevType":1,"Addr":"rtsp://10.58.122.170:554/MainStream","UserName":"admin","Passwd":"154vDmYO2qCYwP5+gusOiA=="}}}
    addRtspStream_req["Message"]["ChnInfo-Properties"]["Addr"] = rtspAddr
    addRtspStream_req =json.dumps(addRtspStream_req)
    ws.send(addRtspStream_req)  ##发送消息
    result = ws.recv()  ##接收消息
    result = json.loads(result)
    if result["RetCode"] == 0:
        print(str(datetime.now()) + "：添加%s视频流成功"%indx)
    else:
        print(str(datetime.now()) + "：添加%s视频流失败：%s" %(indx,result))
        sys.exit()

#查询视频流
def queryRtspStream(ws):
    queryRtspStream_req = """{"Method": "GetConfig", "Page": "ChnInfo"}"""
    ws.send(queryRtspStream_req)  ##发送消息
    result = ws.recv()  ##接收消息
    result = json.loads(result)
    if result["RetCode"] == 0:
        print(str(datetime.now())+"：查询视频流成功")
    else:
        print(str(datetime.now())+"：查询视频流失败：%s"%result)
        sys.exit()
    idxs = json.loads(result["Message"])["ChnInfo-Properties"]
    ChnIdxList = []
    for idx in range(len(idxs)):
        ChnIdxList.append(idxs[idx]["ChnIdx"])
    return ChnIdxList

#删除视频流
def delRtspStream(ws,ChnIdxList):
    for n in ChnIdxList:
        delRtspStream_req = {"Method": "SetConfig", "Page": "ChnInfo",
                         "Message": {"ChnInfo-Properties": {"OpType": 1, "ChnIdx": [n]}}}
        delRtspStream_req = json.dumps(delRtspStream_req)
        ws.send(delRtspStream_req)  ##发送消息
        result = ws.recv()  ##接收消息
        result = json.loads(result)
        if result["RetCode"] == 0:
            print(str(datetime.now()) + "：删除所有视频流成功")
        else:
            print(str(datetime.now()) + "：删除视频流失败：%s" % result)
            sys.exit()

def logOut(ws):
    logOutReq = """{"Method":"Logout","Page":"Logout"}"""
    ws.send(logOutReq)
    result = ws.recv()
    result = json.loads(result)
    if result["RetCode"] == 0:
        print(str(datetime.now())+"：退出盒子管理界面成功")
    else:
        print(str(datetime.now())+"：退出盒子管理界面失败：%s"%result)
        sys.exit()

def initFolder(out,outbak,tmpIdxList):
    if os.path.exists(out):
        shutil.rmtree(out)
        os.makedirs(out)
        for tmp in tmpIdxList:
            dir = out + tmp
            os.makedirs(dir)
    if os.path.exists(outbak):
        shutil.rmtree(outbak)
        os.makedirs(outbak)

#获取视频流抓拍照片名称
def getCaptureImageName(CaptureFileDir):
    ImageNameList = os.listdir(CaptureFileDir)
    captureImageNameList = []
    for name in ImageNameList:
        if '_lrtb' in name:
            captureImageNameList.append(name)

    return captureImageNameList

#创建目录
def makeDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)
        time.sleep(3)
        os.makedirs(dir)
    print("创建目录完成：%s"%dir)

#备份盒子抓拍图片目录
def outBak(boxCaptureOut,boxCaptureOutBak,tmpIdxList,cycleNumber):
    src = boxCaptureOut
    dst = boxCaptureOutBak + 'out_'+ str(cycleNumber) +'/'
    if os.path.exists(dst):
        shutil.rmtree(dst)
        shutil.move(src, dst)
        for tmp in tmpIdxList:
            dir = boxCaptureOut + tmp
            os.makedirs(dir)
    else:
        shutil.move(src,dst)
        for tmp in tmpIdxList:
            dir = boxCaptureOut + tmp
            os.makedirs(dir)
    print("抓拍目录out备份完成")
    return dst

#在ppcluster上添加人员组
def add_personGroup(host,tenantid):
    url = host + '/tenant/' + tenantid + '/person_group'
    redata = {'name': 'xg_person_group'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
    }
    add_person_group= requests.post(url, headers=headers,data=redata)
    person_group_id = add_person_group.json()["data"]["id"]
    print("创建人脸分组，pgid:%s"%person_group_id)
    return person_group_id

#在ppcluster上添加人员
def add_basePerson(host,tenantid,basePersonNameList):
    basePersonIdList =[]
    url = host+'/tenant/'+tenantid+'/person'
    for name in basePersonNameList:
        redata = {'name':name}
        headers = {
            'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
        }
        addperson = requests.post(url,headers=headers,data=redata)
        basePersonIdList.append(addperson.json()['data']['id'])
    # print("增加底库人员，basePersonIdList:%s" % basePersonIdList)
    return basePersonIdList

#在ppcluster上将人员和人员组进行关联
def person_and_personGroup(host,tenantid,person_group_id,basePersonIdList):
    for pid in basePersonIdList:
        url = host+'/tenant/'+tenantid+'/person_group/'+person_group_id+'/person/'+pid
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
        }
        requests.post(url,headers=headers)
    print("人员组绑定完成")

#在ppcluster上为人员添加底库照片
def upload_image_of_basePerson(pplusterUrl,tenantid,basePersonIdList,baseImageNameList,baseImageDir):
    print("开始上传人脸照片")
    for pid,pname in zip(basePersonIdList,baseImageNameList):
        url = pplusterUrl + '/tenant/' + tenantid + '/person/' +pid+ '/face'
        payload = {'policy': 'largest'}
        headers = {
            'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
        }
        faceImage = [('image', open(os.path.join(baseImageDir,pname), 'rb'))]
        r = requests.post(url,headers=headers,data = payload,files=faceImage).json()
    print("上传人脸照片完成")

#将盒子抓拍的照片在ppcluster上搜索相应人员底库的照片
def search_image_from_personGroup(host,tenantid,person_group_id,CaptureFileDir,CapturePersonNameList,threshold,search_retsFile):
    url = host + '/tenant/' + tenantid + '/person_group/'+ person_group_id + '/search'
    search_retsList = []
    num = 1
    for captureImageName in CapturePersonNameList:
        #f = os.path.join(CaptureFilePath, captureImageName)
        captureImageFile = os.path.join(CaptureFileDir,captureImageName)
        # print("开始上传抓拍图进行搜索匹配%d：%s"%(num,captureImageName))
        num += 1
        CaptureFaceImage = [('image', open(captureImageFile, 'rb'))]

        payload = {'top_k': '1','threshold': '0.3','oneface': 'true'}
        headers = {
            'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg=',
        }
        search_rets = requests.post(url, headers=headers,data = payload,files=CaptureFaceImage)
        search_rets = search_rets.json()

        # 将每个抓拍文件搜索响应报文保存到相应的文件当中
        f = captureImageName.split('.')[0] + '_res'+'.txt'
        search_retsResFile = os.path.join(CaptureFileDir,f)
        with open(search_retsResFile,'w') as f:
            f.write(str(search_rets))

        #对响应消息报文进行分析
        if search_rets["code"] != 0:
            search_retsList.append([captureImageName, '', ''])
            print("code 不等于零",search_rets)
            continue
        search_rets = search_rets['data']['search_rets']
        if len(search_rets) <= 0:
            print("search_rets['data']['search_rets'] 小于等于零",search_rets)
            search_retsList.append([captureImageName, '', ''])
            continue
        search_rets = search_rets[0]
        if len(search_rets) <= 0:
            print("search_rets['data']['search_rets'][0] 小于等于零",search_rets)
            search_retsList.append([captureImageName, '', ''])
            continue
        score = search_rets[0]["score"]
        #print("人脸检索匹配置信度：%0.2f"%score)
        basePersonName = search_rets[0]["person_name"]
        #print("人脸检索匹配姓名----------------------------------：%s" % basePersonName)
        search_retsList.append([captureImageName,score,basePersonName])

    #将搜索解析结果保存至文件
    with open(search_retsFile, 'w') as f:
        for r in range(len(search_retsList)):
            f.write(search_retsList[r][0])
            f.write(',')
            f.write(str(search_retsList[r][1]))
            f.write(',')
            f.write(search_retsList[r][2])
            f.write('\n')
    print("上传抓拍图在人脸底库中进行搜索完成")
    return search_retsList

#抓拍照片搜索结果的统计分析
def analyseSearchRes(search_retsList,statisticalResultFile,captureImageNameList):
    found_retslist = [r for r in search_retsList if r[2]]#有匹配结果的
    notfound_retslist = [r for r in search_retsList if not r[2]]#没有匹配到结果
    CaptureNumber = len(captureImageNameList)#抓拍总人数
    basePersonNumber = len(baseImageNameList)#底库总人数
    omissiveNumber = basePersonNumber-len(set([r[2] for r in found_retslist]))#漏抓人数
    TP = [s for s in found_retslist if s[1] > misiThreshold]
    FP = [s for s in found_retslist if s[1] < misiThreshold]
    misiNumber = len(notfound_retslist) +len(FP)#误抓人数
    repeatedNumber = len(found_retslist) - len(set([r[2] for r in found_retslist]))#重复人数
    omissiveRate = omissiveNumber/basePersonNumber#漏检率
    detecRate = 1 - omissiveRate  # 检测率
    repRate = repeatedNumber/basePersonNumber#重复率
    if CaptureNumber ==0:
        print("————————————————————————————没有抓拍到照片,终端后续处理，继续重新开始添加视频流再进行抓拍！——————————————————————————————————")
    misiRate = misiNumber/CaptureNumber#误检率

    #统计结果写文件
    with open(statisticalResultFile,'w') as f:
        f.write("预期检测人数：")
        f.write(str(basePersonNumber))
        f.write('\n')
        f.write("实际检出人数：")
        f.write(str(CaptureNumber))
        f.write('\n')
        f.write("检测率：")
        f.write(str(detecRate))
        f.write('\n')
        f.write("漏检数：")
        f.write(str(omissiveNumber))
        f.write('\n')
        f.write("重复数：")
        f.write(str(repeatedNumber))
        f.write('\n')
        f.write("重复率：")
        f.write(str(repRate))
        f.write('\n')
        f.write("误检数：")
        f.write(str(misiNumber))
        f.write('\n')
        f.write("误检率:")
        f.write(str(misiRate))
        f.write('\n')

    print("预期检出人数：%d" %basePersonNumber)
    print("实际检出人数：%d" %CaptureNumber)
    print("检测率:%f" %detecRate)
    print("漏检数：%d" %omissiveNumber)
    print("漏测率:%f" %omissiveRate)
    print("重复数：%d" %repeatedNumber)
    print("重复率:%f" %repRate)
    print("误检数：%d" % misiNumber)
    print("误检率:%f" %misiRate)
    print("抓拍结果统计分析完成")
    return (detecRate,omissiveRate,repRate,misiRate)

#异常抓拍照片备份
def abnormal_image_backup(baseImageDir,CaptureFileDir,baseImageNameList,omissiveDir,repeateDir,misiDir,search_retsList,misiThreshold):
    # print("search_retsList---------------------------------------",search_retsList)
    found_retslist = [r for r in search_retsList if r[2]]#有匹配结果的
    # print("found_retslist---------------------------------------",found_retslist)
    notfound_retslist = [r for r in search_retsList if not r[2]]#没有匹配到结果
    # print("notfound_retslist---------------------------------------", notfound_retslist)
    #备份漏检照片
    found_retsSet = set([r[2] for r in found_retslist])
    # print("found_retsSet————————————————————————————",found_retsSet)
    basePersonNameSet = set(baseImageNameList)
    # print("basePersonNameSet————————————————————————————",basePersonNameSet)
    omissiveList = list(basePersonNameSet - found_retsSet)
    # print("omissiveList————————————————————————————",omissiveList)
    if len(omissiveList)>0:
        for omissiveName in omissiveList:
            omissiveSrcFile = os.path.join(baseImageDir,omissiveName)
            omissiveDstFile = os.path.join(omissiveDir,omissiveName)
            shutil.copyfile(omissiveSrcFile, omissiveDstFile)

    #备份重复照片
    found_retslist = sorted(found_retslist, key = lambda i: i[2])
    repeated_groups = [(k, list(v)) for k, v in itertools.groupby(found_retslist, lambda i: i[2])]
    repeated_groups = [(k, v) for k, v in repeated_groups if len(v) > 1]
    c = 0
    for group_name, items in repeated_groups:
        gname, _ = os.path.splitext(group_name)
        for item in items:
            file_name = item[0]
            bname, ext = os.path.splitext(file_name)
            new_name = '%s%s' % (bname, ext)
            newName = new_name.split('\\')[-1]
            repeateSrcFile = os.path.join(CaptureFileDir, file_name)
            repeateDstFile = os.path.join(repeateDir, newName)
            shutil.copyfile(repeateSrcFile, repeateDstFile)
            c += 1

    #备份误检照片
    if len(notfound_retslist) > 0:
        for misiName in notfound_retslist:
            misiSrcFile = os.path.join(CaptureFileDir, misiName[0])
            misiDstFile = os.path.join(misiDir, misiName[0])
            shutil.copyfile(misiSrcFile, misiDstFile)
    misiList = []
    for misiName in found_retslist:
        if misiName[1] < misiThreshold:
            misiList.append(misiName[0])
    #print(misiList)
    if len(misiList)>0:
        for misiName in misiList:
            misiSrcFile = os.path.join(CaptureFileDir, misiName)
            misiDstFile = os.path.join(misiDir, misiName)
            shutil.copyfile(misiSrcFile, misiDstFile)
    print("备份各种异常抓拍照片成功")

#将抓拍统计的结果同步到InfluxDB数据库中
def collectDataToInfluxDB(cameraIp,type,tmpIdx,detecRate,omissiveRate,repRate,misiRate):
    data_list = [{
        'measurement': 'normalCameraFaceCapture',
        'tags': {'cameraIP': cameraIp,
                 'tmpIdx': tmpIdx,
                  'Type':type},
        'fields': {
            'detecRate': detecRate,
            'omissiveRate': omissiveRate,
            'repRate': repRate,
            'misiRate': misiRate,
        },
    }]
    return data_list

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(funcName)s - %(message)s')
    localIP = '10.58.122.65'

    cameraIPList = ["10.58.122.171","10.58.122.172"]
    cameraTypeList = ["dongshi","haikang"]
    tmpIdxList = ['tmp_0','tmp_1']
    #cameraIPdict = {"10.58.122.201": 'yushi', "10.58.122.202": 'haikang'}
    cameraCaptureOut = '/data/zcm_hezi/ws_client_01/ws_client/out/'
    cameraCaptureOutBak ='/data/zcm_hezi/ws_client_01/ws_client/outbak/'
    initFolder(cameraCaptureOut, cameraCaptureOutBak, tmpIdxList)

    baseImageDir = '/data/zcm_hezi/baseImage'
    baseImageNameList = os.listdir(baseImageDir)
    #RtspStreamTime = 65

    pplusterUrl = 'http://10.58.150.6:9090'
    tenantid = 'a7f4e146'
    searchThreshold = 0.3
    misiThreshold = 0.3
    person_group_id = add_personGroup(pplusterUrl, tenantid)
    basePersonIdList = add_basePerson(pplusterUrl, tenantid, baseImageNameList)
    person_and_personGroup(pplusterUrl, tenantid, person_group_id, basePersonIdList)
    upload_image_of_basePerson(pplusterUrl,tenantid,basePersonIdList,baseImageNameList,baseImageDir)

    influxDBIP = '10.58.150.5'
    client = InfluxDBClient(influxDBIP, 8086, database="algDataCollection")

    cycleNumber = 1
    maxCycleNum = 500
    s = sokcetServer(localIP)
    sock, addr = s.accept()
    print("已经连接，等待视频播放完成")

    while True:
        try:
            buf = sock.recv(1024)  # 接收数据
            buf = buf.decode()  # 解码
            if buf == "over":
                print("视频抓拍完成，开始进行抓拍分析")
                time.sleep(10)
                # 抓拍完成后先把抓拍文件备份
                outBakDir = outBak(cameraCaptureOut, cameraCaptureOutBak, tmpIdxList, cycleNumber)
                #抓拍结果统计分析
                for cameraIp, cameratype,tmpIdx in zip(cameraIPList, cameraTypeList,tmpIdxList):

                    search_retsFile = outBakDir + tmpIdx + '_res' + '/searchResFile.txt'
                    statisticalResultFile = outBakDir + tmpIdx + '_res' + '/statisticalResFile.txt'
                    misiDir = outBakDir + tmpIdx + '_res' + '/misiDir'
                    makeDir(misiDir)
                    omissiveDir = outBakDir + tmpIdx + '_res' + '/omissiveDir'
                    makeDir(omissiveDir)
                    repeateDir = outBakDir + tmpIdx + '_res' + '/repeateDir'
                    makeDir(repeateDir)

                    CaptureFileDir = outBakDir + tmpIdx
                    captureImageNameList = getCaptureImageName(CaptureFileDir)
                    print("captureImageNameList-------------------------------------------------", captureImageNameList)
                    search_retsList = search_image_from_personGroup(pplusterUrl, tenantid, person_group_id,
                                                                    CaptureFileDir, captureImageNameList,
                                                                    searchThreshold, search_retsFile)
                    detecRate, omissiveRate, repRate, misiRate = analyseSearchRes(search_retsList,
                                                                                  statisticalResultFile,
                                                                                  captureImageNameList)
                    abnormal_image_backup(baseImageDir, CaptureFileDir, baseImageNameList, omissiveDir, repeateDir,
                                          misiDir, search_retsList, misiThreshold)

                    client.write_points(
                        collectDataToInfluxDB(cameraIp,cameratype, tmpIdx, detecRate, omissiveRate, repRate, misiRate))
                    print("——————————————————————————%s摄像机，%s视频流循环播放抓拍：%d次统计分析完成————————————————————" % (
                    cameraIp, tmpIdx, cycleNumber))
            cycleNumber += 1
            if cycleNumber <= maxCycleNum:
                data = "over"  # 输入要传输的数据
                sock.send(data.encode())  # 将要传输的数据编码发送，如果是字符数据就必须要编码发送
                print('通知终端继续播放视频')
                continue
            else:
                data = "gameOver"  # 输入要传输的数据
                sock.send(data.encode())  # 将要传输的数据编码发送，如果是字符数据就必须要编码发送
                print("通知终端停止视频播放")
                break
        except Exception as e:
            print(str(datetime.now()) + "：抓拍处理异常————————————：%s" % e)
            traceback.print_exc(e)
            cycleNumber += 1
            continue