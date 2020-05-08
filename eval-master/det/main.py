import configparser

from eval_ap import *

import numpy as np
import json
from xml.dom.minidom import parse
import xmltodict
from terminaltables import AsciiTable
import os
import matplotlib.pyplot as plt
import shutil
cfg = "./config.py"
config_raw = configparser.RawConfigParser()
config_raw.read(cfg)

defaults = config_raw.defaults()

txt_file = eval(config_raw.get('main_cfg', 'txt_file'))
root_path = eval(config_raw.get('main_cfg', 'root_path'))
_ind_to_cate = eval(config_raw.get('main_cfg', '_ind_to_cate'))
all_iou_thr = eval(config_raw.get('main_cfg', 'all_iou_thr'))
pr_curve = eval(config_raw.get('main_cfg', 'pr_curve'))
pr_precision = eval(config_raw.get('main_cfg', 'pr_precision'))
image_file =eval(config_raw.get('main_cfg', 'image_file'))
if_vil = eval(config_raw.get('main_cfg', 'if_vil'))
vil_iou = eval(config_raw.get('main_cfg', 'vil_iou'))
if_gt = eval(config_raw.get('main_cfg', 'if_gt'))
mini_size = eval(config_raw.get('main_cfg', 'mini_size'))

def main():
	
	_cate_to_ind = {value:key for key,value in _ind_to_cate.items()}
	num_cls = len(_ind_to_cate.keys())

	all_image_res = get_res(num_cls,txt_file,root_path,_ind_to_cate)

	all_gt_bbox, all_gt_label, all_gt_ignore = get_gt(txt_file,root_path,_cate_to_ind,mini_size=mini_size)

	map_results = np.empty(shape=[len(all_iou_thr),num_cls])

	
	if pr_curve==True:
		if os.path.exists("./pr_cruve"):
			shutil.rmtree('./pr_cruve')
		for k in range(num_cls):
			for i in range(len(all_iou_thr)):
				mean_ap, eval_results = eval_map(txt_file,all_image_res,all_gt_bbox,all_gt_label,_ind_to_cate=_ind_to_cate,iou_thr=all_iou_thr[i],gt_ignore=all_gt_ignore)
				per_ap = eval_results[k]['ap']
				list_key = list(_ind_to_cate.keys())
				key = list_key[k]
				title_name = _ind_to_cate[key]+'-'+'iou='+str(all_iou_thr[i])
				a = eval_results[k]
				recall = list(a['recall'])
				precision = list(a['precision'])
				#print_pr_curve(title_name,root_path,_ind_to_cate,all_iou_thr,recall,precision,ap = per_ap,pr_precision=pr_precision)
				print_pr_curve(title_name,_ind_to_cate,recall,precision,ap = per_ap,pr_precision=pr_precision)
				
				for j in range(num_cls):
					map_results[i,j] = eval_results[j]['ap']
		cat = list(_cate_to_ind.keys())
		summary_all_results(cat,map_results,thr_iou= all_iou_thr)

	else:
		for i in range(len(all_iou_thr)):
			mean_ap, eval_results = eval_map(txt_file,all_image_res,all_gt_bbox,all_gt_label,_ind_to_cate=_ind_to_cate,iou_thr=all_iou_thr[i],gt_ignore=all_gt_ignore)
			for j in range(num_cls):
				map_results[i,j] = eval_results[j]['ap']

		cat = list(_cate_to_ind.keys())
		summary_all_results(cat,map_results,thr_iou= all_iou_thr)

	if if_vil == True:
		visualize(txt_file,vil_iou,image_file,if_gt)


main()


