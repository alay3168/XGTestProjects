#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @auther:suzhao
# @date:2018.8.7


import csv
import json
import requests
import time
import unittest

from typing import Tuple


def readerCSV(filename):
	# type: (object) -> object

	datas = []

	with open(filename,'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		data = {}
		for row in reader:
			data['id'] = row['id']
			data['image1'] = row['image1']
			data['type'] = row['type']
			data['attribute'] = row['attribute']
			data['name'] = row['name']
			data['id_no'] = row['id_no']
			data['tel'] = row['tel']
			data['age'] = row['age']
			datas.append(data)
			print datas


			return datas


if __name__ == '__main__':
	readerCSV('csv_data.csv')






