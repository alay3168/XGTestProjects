#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import telnetlib
# tyztgg_Iplist =[]
# hzmjyz_Iplist =[]
# cdhtmz_Iplist =[]
# tzjlda_Iplist =[]
# zyjlgj_Iplist =[]
# tyztgg_Iplist =[]
# tyztgg_Iplist =[]
# tyztgg_Iplist =[]
# tyztgg_Iplist =[]
# tyztgg_Iplist =[]
# tyztgg_Iplist =[]
# tyztgg_Iplist =[]

def sub_str(s,star,end):
    i = 1
    j = 1
    ss = ''
    sl = []
    while i:
        if i <len(s)-1:
            if s[i-1] == star:
                while True:
                    if s[j] !=end:
                        ss = ss + s[j]
                        j =j + 1
                    else:
                        i = j+1
                        j = j+1
                        break
                sl.append(ss)
                ss = ''
            else:
                i = i+1
                j = j +1
                continue
        else:
            break
    return sl

with open('fwInfo.txt','r',encoding='utf-8') as f:
    ipList = f.read()
aa = ipList.split('\n#')
# print(aa)
bb = []
for i in range(len(aa)):
    bb.append(aa[i].split('-----------------------'))
# print(bb)
# # # print(len(bb))
cc = []
dd = []
for i in range(len(bb)):
    if i == 0:
        continue
    ss = bb[i][1]
    print(sub_str(ss,'\n','\t'))
    print('')
    # dd = dd +cc
print(cc)
# bb= ss.split('-----------------------')
# cc = aa[1].split('\n')
# dd =[]
# ee = []
# print(len(bb))
# for i in range(len(bb)):
#     if '\t' in bb[i]:
#         cc.append(bb[i].split('\t'))
#
# for i in range(len(cc)):
#     dd.append(cc[i][0])

# print(dd)
# print(bb)
# print('--------------------------')
#
# import re
# list = []
# list2 = []
# print(type(list2))
# list3 = []
# for i in range(len(ip)):
#     ss = ip[i].split('-----------------------')
#     list2 = list.append(i)
# print(type(list2))
# for j in range(len(list2)):
#     list3 = re.split('\t|\n',list2[j][1])
#
# print(list3)

# print(list)
# import re
#
# a = "\n10.10.40.247\t1.0.11.20190924\n10.10.40.248\t1.0.11.20190924\n"
# # print(a.split('\n'))
# print(re.split('\t|\n',a))

