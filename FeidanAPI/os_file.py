#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2019-8-28
# @Description: FEIDAN_API
#****************************************************************
import os
# file_dir = r"D:\\face1"
# i = 1
# a = os.walk(file_dir)
# for root, dirs, files in os.walk(file_dir):
#     print(i)
#     i += 1
#     # print(root) #当前目录路径
#     # print(dirs) #当前路径下所有子目录
#     # print(files) #当前路径下所有非目录子文件
#     filename = files
#     print(','.join(filename))

#*************************************
f = file(r'D:\filname.txt', 'r') #打开文件
txt = f.read() #读出文件内容
f.close()
a = txt.replace(',', '\n') #将逗号替换换行
print a

#****************************************************************
# import os
# path = 'D:\\face1'
# filelist = os.listdir(path)
# for item in filelist:
#         #print('item name is ',item)
#         if item.endswith('.jpg'):
#                 # name = item.split('_',3)[0] + '.' + item.split('.',3)[1]
#                 name = item.split('_',1)[0].replace('10.58.7.112','10.58.7.103') + '_'+ item.split('_',1)[1]
#
#                 src = os.path.join(os.path.abspath(path),item)
#                 dst = os.path.join(os.path.abspath(path),name)
#         try:
#                 os.rename(src,dst)
#                 print('rename from %s to %s'%(src,dst))
#         except:
#                 continue

