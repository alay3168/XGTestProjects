#!/usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************
# @Author     : suzhao
# @Version    : 1.0
# @Date       : 2018-8-08
# @Description: 智能监控平台API
#****************************************************************

import xlrd
class ReadExcel():
	def __init__(self, excelPath, sheetName="Sheet1"):
		self.data = xlrd.open_workbook(excelPath)
		self.table = self.data.sheet_by_name(sheetName)
		# # 获取第一行作为key值
		# self.keys = self.table.row_values(0)
		# 获取总行数
		self.rowNum = self.table.nrows
		# 获取总列数
		self.colNum = self.table.ncols

	def dict_data(self):
		user = []
		for i in range(self.rowNum):
			# if i == 0:
			# 	continue
			values = self.table.row_values(i)
			# print self.table.row_values(i)
			user.append(self.table.row_values(i))
		print user


if __name__ == "__main__":
	filepath = "staff_api.xlsx"
	sheetName = "Sheet1"
	data = ReadExcel(filepath, sheetName)
	data.dict_data()


