#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2018-8-08
# @Description: 传图工具
#****************************************************************

from common import img_setup
import unittest
import requests
import json
import sys
import base64
import os

class WebimageTestCase(img_setup.ImageTest):

    def md5(self,pic_path,timestamp, cam_info):

        img_b64 = ''

        with open(pic_path, 'rb') as fin:
            image_data = fin.read()
            img_b64 = base64.b64encode(image_data)
            print "encode data"

        # get_md5 = "camera_uuid=%s&day_night=day&face_body=face&image=%s&image_name=%s&time=%s&code=123456" % (
        #     cam_info, img_b64, img_name, timestamp)
        #
        # md5 = hashlib.md5()
        # md5.update(get_md5)
        # md5_res = md5.hexdigest()

    def test_img_case(self):
        get_md5 = "camera_uuid=%s&day_night=day&face_body=face&image=%s&image_name=%s&time=%s&code=123456" % (
            cam_info, img_b64, img_name, timestamp)

        md5 = hashlib.md5()
        md5.update(get_md5)
        md5_res = md5.hexdigest()

        params = {
            "access_token": md5_res,
            "index": "10000"}
        payload = {
            "camera_uuid": (None, cam_info),
            "day_night": (None, "day"),
            "face_body": (None, "face"),
            "image": (None, img_b64),
            "time": (None, timestamp),
            "path": (None, ""),
            "image_name": (None, img_name)
        }

        r = requests.post(self.url,params=params,data=payload,headers=self.headers, verify=False)
        print r.text


    def url(self, path):
        return self.domain + path




if __name__ == '__main__':

    # unittest.main()
















