#!/usr/bin/env python
import logging
import sys
import os
import argparse
import json
import time
import requests
import base64
import hashlib
import glob
import threading

HOMEY_ADDRRESS = ""
#HOMEY_ADDRRESS = "http://10.58.150.5:9104"

logging.basicConfig(level=logging.DEBUG)


def upload(client, pic_path, timestamp, cam_info):
    img_b64 = ''

    with open(pic_path, 'rb') as fd:
        data = fd.read()
        img_b64 = base64.b64encode(data)

    header = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Connection': 'Keep-Alive'
    }
    img_name = os.path.basename(pic_path)

    #cam_info = "c902a939-c1f0-4c14-8b48-b85c6daf1476"

    to_md5 = "camera_uuid=%s&day_night=day&face_body=face&image=%s&image_name=%s&time=%s&code=123456" % (
        cam_info, img_b64, img_name, timestamp)

    md5 = hashlib.md5()
    md5.update(to_md5)
    md5_res = md5.hexdigest()

    url = "%s/api/v1/imagelogs/logs" % (HOMEY_ADDRRESS)

    params = {
        "access_token": md5_res,
        "index": "10000"
    }

    data = {
        "camera_uuid": (None, cam_info),
        "day_night": (None, "day"),
        "face_body": (None, "face"),
        "image": (None, img_b64),
        "time": (None, timestamp),
        "path": (None, ""),
        "image_name": (None, img_name)
    }

    logging.info("load image_file:%s, image_name:%s", pic_path, img_name)

    resp = client.post(url, params=params, files=data, verify=True)

    logging.info("code=%d,msg=%s", resp.status_code, resp.content)

    try:
        pass
        # os.remove(pic_path)
    except:
        logging.error("could not remove file %s", pic_path)


def get_file_mtime(file_path):
    try:
        stat = os.stat(file_path)
    except Exception as e:
        raise e

    return "%f" % stat.st_mtime



files = glob.glob("/data/face/face/*.jpg")

from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        self.i = 0

    @task(1)
    def baidu(self):
        f = files[self.i]
        self.i = (self.i + 1) % len(files)
        epoch = get_file_mtime(f)
        upload(self.client, f, epoch, "00000000-0000-0000-0000-000000000001")
        #self.client.get("/")



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
#    min_wait = 3000
#   max_wait = 6000
