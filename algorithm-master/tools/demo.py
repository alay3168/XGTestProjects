import numpy as np  
import sys,os  
import cv2
sys.path.insert(0, "../caffe/python")
os.environ['GLOG_minloglevel'] = '2'  
import caffe  
from transform import bbox_transform_inv
from anchor_generator import AnchorGenerator

from facedet_v import facecdet as detcfg

def preprocess(src,im_cfg):
    im = cv2.resize(src, im_cfg['shape'])
    im = im[...,::-1]
    im = (im - im_cfg['mean']) / im_cfg['std']
    im = im.transpose(2, 0, 1)
    im = im[np.newaxis,:]
    return im

def py_nms(dets, scores_, thresh):
    """Pure Python NMS baseline."""
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = scores_.ravel()
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h

        ovr = inter / (areas[i] + areas[order[1:]] - inter)
      
        inds = np.where(ovr <= thresh)[0]

        order = order[inds + 1]
    return dets[keep],scores_[keep]

def get_anchor(anchor_cfg, img_shape):
    stride = anchor_cfg['stride']
    scale = anchor_cfg['scale']
    ratio = anchor_cfg['ratio']
    anchors = np.ones((0,4))
    for i in range(len(stride)):
        s = stride[i]
        base = AnchorGenerator(base_size=s,scales=scale,ratios=ratio)
        anchor = base.grid_anchors([img_shape[0]/s,img_shape[1]/s],stride=s)
        anchors = np.concatenate((anchors,anchor),axis=0)
    return anchors

def detect(imgfile,cfg):
    origimg = cv2.imread(imgfile)
    img = preprocess(origimg,cfg['img_preprocess'])
    
    img = img.astype(np.float32)
    net.blobs['data'].reshape(*img.shape)
    net.blobs['data'].data[...] = img
    out = net.forward()

    anchors = get_anchor(cfg['anchor'],img.shape[2:])
    scores= out['mbox_sigmoid'][0]
    bbox_pred = out['mbox_reg'][0].reshape(-1,4)
    topk_inds = np.where(scores>=cfg['process']['score'])[0]
    anchors = anchors[topk_inds, :]
    bbox_pred = bbox_pred[topk_inds, :]
    scores = scores[topk_inds, :]
    bboxes = bbox_transform_inv(anchors, bbox_pred)
    box, det_scores = py_nms(bboxes, scores, cfg['process']['nms_thre'])
    box[:,::2] = box[:,::2] * origimg.shape[1]/img.shape[3]
    box[:,1::2] = box[:,1::2] * origimg.shape[0]/img.shape[3]
    if cfg['vis_detresult'] == True:
        for i in range(len(box)):
            p1 = (int(box[i][0]), int(box[i][1]))
            p2 = (int(box[i][2]), int(box[i][3]))      
            cv2.rectangle(origimg, p1, p2, (0,255,0))
            p3 = (max(p1[0], 15), max(p1[1], 15))
            title = "%.2f" % (det_scores[i])
            cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (0, 255, 0), 1)
        cv2.imshow("detect", origimg)
         
        k = cv2.waitKey(0) & 0xff
               #Exit if ESC pressed
        if k == 27 : return False
    with open(imgfile.split('.')[0]+".txt","w") as f:
        for i in range(len(box)):
            for j in range(4):
                f.write(str(box[i][j])+" ")
            f.write("1 " + "%.2f" % (det_scores[i]))
            f.write('\n')
    return True



if __name__ == "__main__":
    deploy = cfg['facedet_v']['deploy']
    model = cfg['facedet_v']['model']

    if not os.path.exists(deploy):
        print(deploy + " does not exist")
    if not os.path.exists(model):
        print(model + " does not exist")

    caffe.set_mode_cpu() 
    net = caffe.Net(deploy,model,caffe.TEST) 
    params = net.params
    caffemodel = 'caffe_inference.caffemodel' 
    net.save(caffemodel)  
    with open(cfg['test_imglist']) as f:
        lines = f.readlines()
    for i in range(len(lines)):
        img_ = lines[i].strip().split()[0]
        detect(img_,cfg)
