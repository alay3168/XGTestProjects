[main_cfg]

# the input txt (res-gt)
txt_file = './data/res_gt.txt'

root_path = './'

# category map
_ind_to_cate = {0: 'person_normal'}
#, 1: 'visperson_normal', 2: 'person_cycling', 3: 'person_others', 4: 'visperson_cycling'}

# evaluate the ap of all_iou_thr
all_iou_thr = [0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]

# evaluate min_size of bbox 
mini_size = 50*50

# if print the pr-curve (True or False)
pr_curve=True

# when pr-curve = True, the precision shown on the pr-curve
# if pr-curve = False, just ignore this parameter(pr_precision)
pr_precision=[0.7,0.8,0.9,0.99]

# when visualize the results and gt, the images are needed
# path of the images
image_file = './data'

# when iou in vil_iou, visualize the results of detect
if_vil = False
# if if_vil = False, just ignore this parameter(vil_iou)
vil_iou = [0.4]
# if if_vil = False, just ignore this parameter
# this parameter means whether visualize the ground-truth bboxes
if_gt = True
