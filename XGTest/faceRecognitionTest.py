import os
import random
import time
from random import shuffle

import requests


# 在ppcluster上添加人员组
def add_personGroup(host, tenantid):
    url = host + '/tenant/' + tenantid + '/person_group'
    redata = {'name': 'xg_person_group'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
    }
    add_person_group = requests.post(url, headers=headers, data=redata)
    person_group_id = add_person_group.json()["data"]["id"]
    print("创建人脸分组，pgid:%s" % person_group_id)
    return person_group_id


# 在ppcluster上添加人员
def add_basePerson(host, tenantid, basePersonNameList):
    basePersonIdList = []
    url = host + '/tenant/' + tenantid + '/person'
    print("开始注册人员名称")
    for name in basePersonNameList:
        redata = {'name': name}
        headers = {
            'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
        }
        addperson = requests.post(url, headers=headers, data=redata)
        basePersonIdList.append(addperson.json()['data']['id'])
    # print("增加底库人员，basePersonIdList:%s" % basePersonIdList)
    print("注册人员名称完成")
    return basePersonIdList


# 在ppcluster上将人员和人员组进行关联
def person_and_personGroup(host, tenantid, person_group_id, basePersonIdList):
    print("开始人员与人员组进行绑定")
    for pid in basePersonIdList:
        url = host + '/tenant/' + tenantid + '/person_group/' + person_group_id + '/person/' + pid
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
        }
        requests.post(url, headers=headers)
    print("人员组绑定完成")


# 注册人脸照片
def faceRegistered(pplusterUrl, tenantid, basePersonIdList, baseFaceImageNameList, baseFaceImageDir, G, B, ):
    print("开始注册人脸照片")
    for pid, pname in zip(basePersonIdList, baseFaceImageNameList):
        print('-', end='')
        url = pplusterUrl + '/tenant/' + tenantid + '/person/' + pid + '/face'
        # print(url)
        payload = {'policy': 'largest'}
        headers = {
            'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg='
        }
        faceImage = [('image', open(os.path.join(baseFaceImageDir, pname), 'rb'))]
        r = requests.post(url, headers=headers, data=payload, files=faceImage).json()
        if r["code"] == 0:
            G = G + 1
        else:
            B = B + 1
    print("开始注册人脸照片完成")
    # 注册失败率：
    BP = B / (G + B)
    print('注册失败率BP: {:.2f}%'.format(BP * 100))


# 人脸识别（即上传测试对象照片与注册人脸照片进行对比识别）
def faceRecognitionTest(pplusterUrl, tenantid, person_group_id, searchThresholdList):
    url = pplusterUrl + '/tenant/' + tenantid + '/person_group/' + person_group_id + '/search'
    fpList = []
    lpList = []
    trList = []
    for searchThreshold in searchThresholdList:

        # #随机打乱fullTestFaseImageNameDirList顺序
        # shuffle(fullTestFaseImageNameDirList)
        num = 1
        # 测试通行总次数
        N = 0
        # 已列入监视名单名单的测试对象通行测试次数
        R = 0
        # 发生非监视名单测试对象名单误报的通行测试次数
        T = 0

        # 发生监视名单漏报的通行测试次数
        L = 0

        # 系统平均响应时间
        TR = 0
        # 随机记录的第i次告警响应时间
        Ti = 0
        # 随机记录的10次告警响应时间中的最大值
        Tmax = 0
        # 随机记录的10次告警响应时间中的最小值
        Tmin = 0
        # 响应时间记录
        responseTimeList = []
        # 所有测试对象照片(每张监视人员的测试对象进行人脸识别不低于2次，非监视人员测试对象数量不低于监视名单测试照片的2倍，)
        fullTestFaseImageNameDirList = random.choices(baseFaceTestImageNameDirList, k=500) * 2 + random.choices(
            notBaseFaceTestImageNameDirList, k=2000)
        shuffle(fullTestFaseImageNameDirList)
        for FaseImageNameDir in fullTestFaseImageNameDirList:

            # f = os.path.join(CaptureFilePath, captureImageName)
            print("开始上传抓拍图进行搜索匹配%d：%s" % (num, FaseImageNameDir))
            num += 1
            CaptureFaceImage = [('image', open(FaseImageNameDir, 'rb'))]

            payload = {'top_k': '1', 'threshold': searchThreshold, 'oneface': 'true'}
            headers = {
                'Authentication': 'Bearer fnv43QM55SDvcFLYpe_VdC4pgh2WO9BM1n11ALU2-5s.1578381916.qthABm+hcJ4+PwBcK1mBuio8Pbg=',
            }
            starTime = time.time()  # 记录开始时间
            search_rets = requests.post(url, headers=headers, data=payload, files=CaptureFaceImage)
            search_rets = search_rets.json()
            endTime = time.time()  # 记录响应完成时间
            responseTime = endTime - starTime  # 获取每次人脸识别的响应时间间隔
            responseTimeList.append(responseTime)

            # 将搜索响应报文保存到相应的文件当中
            res = FaseImageNameDir.split('.')[0] + '_res1' + '.txt'
            if os.path.exists(res):
                res = FaseImageNameDir.split('.')[0] + '_res2' + '.txt'
                with open(res, 'w') as f:
                    f.write(str(search_rets))
            else:
                with open(res, 'w') as f:
                    f.write(str(search_rets))

            # 对响应消息报文进行分析
            if search_rets["code"] != 0:
                print("code 不等于零", search_rets)
                if baseFaceTestImageDir == os.path.dirname(FaseImageNameDir):
                    # 监视人员测试名单误报的通行次数+1
                    L = L + 1
                continue
            search_rets = search_rets['data']['search_rets']
            if len(search_rets) <= 0:
                print("search_rets['data']['search_rets'] 小于等于零", search_rets)
                if baseFaceTestImageDir == os.path.dirname(FaseImageNameDir):
                    # 监视人员测试名单误报的通行次数+1
                    L = L + 1
                continue
            search_rets = search_rets[0]
            if len(search_rets) <= 0:
                print("search_rets['data']['search_rets'][0] 小于等于零", search_rets)
                if baseFaceTestImageDir == os.path.dirname(FaseImageNameDir):
                    # 监视人员测试名单误报的通行次数+1
                    L = L + 1
                continue
                # 获取识别到的注册人员名称
            person_name = search_rets[0]["person_name"]
            if baseFaceTestImageDir == os.path.dirname(FaseImageNameDir):
                # 已列入监视测试名单人员通行次数+1
                R = R + 1
            if person_name != os.path.basename(FaseImageNameDir):
                print("person_name:%s————————FaseImageName：%s" % (person_name, FaseImageNameDir))
                if notBaseFaceTestImageDir == os.path.dirname(FaseImageNameDir):
                    # 非监视人员测试名单误报的通行次数+1
                    T = T + 1
        print('在特定阈值下各性能指标：', searchThreshold)
        # 测试通行总次数
        N = len(fullTestFaseImageNameDirList)
        # 非监视名单误报率
        FP = T / (N - R)
        fpList.append(FP)
        print('非监视名单误报率FP: {:.2f}%'.format(FP * 100))

        # 已列入监视名单中的测试对象通行测试次数
        R = len(baseFaceTestImageNameDirList * 2)
        # 监视名单漏报率
        LP = L / R
        lpList.append(LP)
        print('监视名单漏报率：{:.2f}%'.format(LP * 100))

        # 随机抽取10条响应时间记录
        randomTimeList = random.choices(responseTimeList, k=10)
        # 从随机抽取的10条记录中获得最大响应时间与最小响应时间以及总时长
        Tmax = max(randomTimeList)
        Tmin = min(randomTimeList)
        sumTime = 0
        for t in randomTimeList:
            sumTime += t
        TR = (sumTime - Tmax - Tmin) / 8
        trList.append(TR)
        print('人脸识别平均响应时间:', TR)
    print("不同阈值下非监视名单误报率列表FP：", fpList)
    print("不同阈值下监视名单漏报率列表LP：", lpList)
    print("不同阈值下平均响应时间列表TR：", trList)


if __name__ == "__main__":

    # 注册人员名单照片
    baseFaceImageDir = 'G:\\faceImage\\test_5000\\base_5000_cropimg'
    baseFaceImageName = os.listdir(baseFaceImageDir)
    baseFaceImageNameList = random.choices(baseFaceImageName, k=5000)  # k不能大于baseFaceImageName长度
    print("监视名单长度：", len(baseFaceImageNameList))

    # 监视名单测试对象照片
    baseFaceTestImageDir = 'G:\\faceImage\\test_5000\\query_5000_cropimg'
    baseFaceTestImageNameList = os.listdir(baseFaceTestImageDir)
    baseFaceTestImageNameDirList = []
    for baseFaceTestImageName in baseFaceTestImageNameList:
        if baseFaceTestImageName.split('.')[1] != 'txt':
            baseFaceTestImageNameDir = os.path.join(baseFaceTestImageDir, baseFaceTestImageName)
            baseFaceTestImageNameDirList.append(baseFaceTestImageNameDir)
    # 非监视名单测试对象照片
    notBaseFaceTestImageDir = 'G:\\faceImage\\test_3000\\q'
    notBaseFaceTestImageNameList = os.listdir(notBaseFaceTestImageDir)
    notBaseFaceTestImageNameDirList = []
    for notBaseFaceTestImageName in notBaseFaceTestImageNameList:
        if notBaseFaceTestImageName.split('.')[1] != 'txt':
            notBaseFaceTestImageNameDir = os.path.join(notBaseFaceTestImageDir, notBaseFaceTestImageName)
            notBaseFaceTestImageNameDirList.append(notBaseFaceTestImageNameDir)

    pplusterUrl = 'http://10.58.150.6:9090'
    tenantid = 'a7f4e146'
    searchThresholdList = [0.5, 0.55, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78]
    # searchThresholdList = [ 0.6]

    # 注册失败率
    BP = 0
    # 注册失败的人脸图像数目
    B = 0
    # 注册成功的人脸图像数目
    G = 0

    person_group_id = add_personGroup(pplusterUrl, tenantid)

    basePersonIdList = add_basePerson(pplusterUrl, tenantid, baseFaceImageNameList)

    person_and_personGroup(pplusterUrl, tenantid, person_group_id, basePersonIdList)

    faceRegistered(pplusterUrl, tenantid, basePersonIdList, baseFaceImageNameList, baseFaceImageDir, G, B)

    faceRecognitionTest(pplusterUrl, tenantid, person_group_id, searchThresholdList)
