#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2018-8-08
# @Description: HOMEY_API
#****************************************************************

import MySQLdb

db = MySQLdb.connect(host='10.58.122.61',port=3310,user='puppy',passwd='123456',db='xgface',charset='utf8')
cursor = db.cursor()

#执行sql语句

sql = "DELETE FROM libraries WHERE id> %s" % 1
try:
   # 执行SQL语句
    cursor.execute(sql)
   # 提交修改
    db.commit()
except:
    db.rollback()

# result = cursor.fetchall()
# print(result)
cursor.close()