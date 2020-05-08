#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
from influxdb import InfluxDBClient


def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    yesterday = yesterday.strftime('%Y%m%d')
    return yesterday

def getFileNames(dir):
    filesList = []
    if os.path.exists(dir):
        for root, dirs, files in os.walk(dir):
            for file in files:
                filesList.append(file)
        return (filesList,len(filesList))
    else:
        return (filesList,0)

def getFtp_puppy(iplist,ftp_puppy):
    for i in range(len(iplist)):
        image_dir = ftp_puppy + iplist[i] + '/' + getYesterday()
        imgList,imgNum = getFileNames(image_dir)
        # all_ip_img_lists.append(imgList)
        client.write_points(image_DataToInfluxDB(iplist[i],imgNum))

def gethomey_puppy(homey_puppy):
    yesterday = getYesterday()
    image_dir  = homey_puppy +  yesterday[0:4] + '/' + yesterday[4:6] + '/' + yesterday[6:8]
    imgList, imgNum = getFileNames(image_dir)
    ipdic = {}
    for img in imgList:
        imgName = img.split('_')
        ip = imgName[0]
        if ip not in ipdic:
            ipdic[ip] = 1
        else:
            ipdic[ip] = ipdic[ip] + 1


#-------------------连接InfluxDB------------------------------
def image_DataToInfluxDB(ip,imgNum):
    data_list = [{
        'measurement': 'image',
        'tags': {'deviceIP': ip},
        'fields': {
            'imgYesterdayNum': imgNum,
        },
    }]
    return data_list


if __name__ == '__main__':
    # imgDir = 'ftp-puppy/10.58.8.16/20200428/10.58.8.16_20200428150520168_YT.jpg'
    '10.58.122.240_20200427224142251_1.jpg'
    ftp_puppy = '/data/homey2.5_200427/ftp/ftp-puppy/'
    homey_puppy = '/data/homey2.5_200427/images_1/camera/face/'
    iplist = ['10.58.8.16','10.58.122.114']
    dbhost = '10.58.150.5'
    client = InfluxDBClient(dbhost, 8086, database="homeySystemMonitor")
    # all_ip_img_lists = []
    getFtp_puppy(iplist, ftp_puppy)


