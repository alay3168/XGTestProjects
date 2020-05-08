import numpy as np 



def imrescale(img, scale, return_scale=True, interpolation='bilinear'):
     """Resize image while keeping the aspect ratio.
 
     Args:
         img (ndarray): The input image.
         scale (float or tuple[int]): The scaling factor or maximum size.
             If it is a float number, then the image will be rescaled by this
             factor, else if it is a tuple of 2 integers, then the image will
             be rescaled as large as possible within the scale.
         return_scale (bool): Whether to return the scaling factor besides the
             rescaled image.
         interpolation (str): Same as :func:`resize`.
 
     Returns:
         ndarray: The rescaled image.
     """
     h, w = img.shape[:2]
     if isinstance(scale, (float, int)):
         if scale <= 0:
             raise ValueError(
                 'Invalid scale {}, must be positive.'.format(scale))
         scale_factor = scale
     elif isinstance(scale, tuple):
         max_long_edge = max(scale)
         max_short_edge = min(scale)
         scale_factor = min(max_long_edge / max(h, w),
                            max_short_edge / min(h, w))
     else:
         raise TypeError(
             'Scale must be a number or tuple of int, but got {}'.format(
                 type(scale)))
     new_size = int(w * float(scale_factor) + 0.5), int(h * float(scale_factor) + 0.5)

     rescaled_img = cv2.resize(
         img, new_size, interpolation=cv2.INTER_LINEAR)

     if return_scale:
         return rescaled_img, scale_factor
     else:
         return rescaled_img

def impad_to_multiple(img, divisor, pad_val=0):
    """Pad an image to ensure each edge to be multiple to some number.

    Args:
       img (ndarray): Image to be padded.
       divisor (int): Padded image edges will be multiple to divisor.
       pad_val (number or sequence): Same as :func:`impad`.

    Returns:
       ndarray: The padded image.
    """
    divisor = float(divisor)
    pad_h = int(np.ceil(img.shape[0] / divisor)) * divisor
    pad_w = int(np.ceil(img.shape[1] / divisor)) * divisor
    return impad(img, (int(pad_h), int(pad_w)), pad_val)

def impad(img, shape, pad_val=0):
    """Pad an image to a certain shape.

    Args:
        img (ndarray): Image to be padded.
        shape (tuple): Expected padding shape.
        pad_val (number or sequence): Values to be filled in padding areas.

    Returns:
        ndarray: The padded image.
    """
    if not isinstance(pad_val, (int, float)):
        assert len(pad_val) == img.shape[-1]
    if len(shape) < len(img.shape):
        shape = shape + (img.shape[-1], )
    assert len(shape) == len(img.shape)
    for i in range(len(shape) - 1):
        assert shape[i] >= img.shape[i]
    pad = np.empty(shape, dtype=np.float64)
    pad[...] = pad_val
    pad[:img.shape[0], :img.shape[1], ...] = img
    return pad, pad.shape



import numpy as np 

def delta2bbox(rois,
                deltas,
                means=[0, 0, 0, 0],
                stds=[1, 1, 1, 1],
                max_shape=None,
                wh_ratio_clip=16 / 1000):
    means = np.repeat(means, deltas.shape[0] // 4)
    stds = np.repeat(stds, deltas.shape[0] // 4)
    denorm_deltas = deltas * stds + means
    dx = denorm_deltas[:, 0::4]
    dy = denorm_deltas[:, 1::4]
    dw = denorm_deltas[:, 2::4]
    dh = denorm_deltas[:, 3::4]
    max_ratio = np.abs(np.log(wh_ratio_clip))
    dw = np.clip(dw,min=-max_ratio, max=max_ratio)
    dh = np.clip(dh,min=-max_ratio, max=max_ratio)
    px = ((rois[:, 0] + rois[:, 2]) * 0.5).unsqueeze(1).expand_as(dx)
    py = ((rois[:, 1] + rois[:, 3]) * 0.5).unsqueeze(1).expand_as(dy)
    pw = (rois[:, 2] - rois[:, 0] + 1.0).unsqueeze(1).expand_as(dw)
    ph = (rois[:, 3] - rois[:, 1] + 1.0).unsqueeze(1).expand_as(dh)
    gw = pw * dw.exp()
    gh = ph * dh.exp()
    gx = torch.addcmul(px, 1, pw, dx)  # gx = px + pw * dx
    gy = torch.addcmul(py, 1, ph, dy)  # gy = py + ph * dy
    x1 = gx - gw * 0.5 + 0.5
    y1 = gy - gh * 0.5 + 0.5
    x2 = gx + gw * 0.5 - 0.5
    y2 = gy + gh * 0.5 - 0.5
    if max_shape is not None:
        x1 = x1.clamp(min=0, max=max_shape[1] - 1)
        y1 = y1.clamp(min=0, max=max_shape[0] - 1)
        x2 = x2.clamp(min=0, max=max_shape[1] - 1)
        y2 = y2.clamp(min=0, max=max_shape[0] - 1)
    bboxes = torch.stack([x1, y1, x2, y2], dim=-1).view_as(deltas)
    return bboxes

def bbox_transform_inv(boxes, deltas,max_shape=None):
     # boxes, deltas and pred_boxes has the same shape: (h*w*a, 4), order: (H,W,A)
    # boxes: anchor boxes
    # deltas: pred_deltas_boxes
    if boxes.shape[0] == 0:
        return np.zeros((0, deltas.shape[1]), dtype=deltas.dtype)
    # astype default will copy
    boxes = boxes.astype(deltas.dtype, copy=False)
 
    widths = boxes[:, 2] - boxes[:, 0] + 1.0
    heights = boxes[:, 3] - boxes[:, 1] + 1.0
    ctr_x = boxes[:, 0] + 0.5 * widths - 0.5
    ctr_y = boxes[:, 1] + 0.5 * heights - 0.5
 
   # dx shape: (N,1)
    dx = deltas[:, 0::4]
    dy = deltas[:, 1::4]
    dw = deltas[:, 2::4]
    dh = deltas[:, 3::4]
 
    pred_ctr_x = dx * widths[:, np.newaxis] + ctr_x[:, np.newaxis]
    pred_ctr_y = dy * heights[:, np.newaxis] + ctr_y[:, np.newaxis]
    pred_w = np.exp(dw) * widths[:, np.newaxis]
    pred_h = np.exp(dh) * heights[:, np.newaxis]
 
    pred_boxes = np.zeros(deltas.shape, dtype=deltas.dtype)
    # print('pred_shape', pred_boxes.shape)
    # x1
    pred_boxes[:, 0::4] = pred_ctr_x - 0.5 * pred_w+0.5
    # y1
    pred_boxes[:, 1::4] = pred_ctr_y - 0.5 * pred_h+0.5
    # x2
    pred_boxes[:, 2::4] = pred_ctr_x + 0.5 * pred_w-0.5
    # y2
    pred_boxes[:, 3::4] = pred_ctr_y + 0.5 * pred_h-0.5
      # BUG: pred_boxes[:,3]-pred_boxes[:,1] != pred_h-1
    if max_shape is not None:
        pred_boxes[:, 0::4] = np.clip(pred_boxes[:, 0::4], 0, max_shape[1] - 1)
        pred_boxes[:, 1::4] = np.clip(pred_boxes[:, 1::4], 0, max_shape[0] - 1)
        pred_boxes[:, 2::4] = np.clip(pred_boxes[:, 2::4], 0, max_shape[1] - 1)
        pred_boxes[:, 3::4] = np.clip(pred_boxes[:, 3::4], 0, max_shape[0] - 1) 
    return pred_boxes

def get_bboxes_single(cls_scores,
                      bbox_preds,
                      mlvl_anchors,
                      img_shape,
                      scale_factor,
                      rescale=True):
    assert len(cls_scores) == len(bbox_preds) == len(mlvl_anchors)
    mlvl_bboxes = []
    mlvl_scores = []
    mlvl_index = []
    for cls_score, bbox_pred, anchors in zip(cls_scores, bbox_preds,
                                             mlvl_anchors):
        assert cls_score.shape[-2:] == bbox_pred.shape[-2:]
        cls_score = cls_score.transpose(1, 2, 0).reshape(-1, 1)
        scores = 1 / (1 + np.exp(-cls_score))
        bbox_pred = bbox_pred.transpose(1, 2, 0).reshape(-1, 4)
        topk_inds = np.where(scores>=0.3)[0]
        anchors = anchors[topk_inds, :]
        bbox_pred = bbox_pred[topk_inds, :]
        scores = scores[topk_inds, :]
        bboxes = bbox_transform_inv(anchors, bbox_pred,img_shape)       
        mlvl_bboxes.append(bboxes)
        mlvl_scores.append(scores)
        for j in range(bboxes.shape[0]):
            mlvl_index.append(i)

    mlvl_bboxes = np.concatenate(mlvl_bboxes)
    mlvl_scores = np.concatenate(mlvl_scores)
    return mlvl_bboxes, mlvl_scores, mlvl_index
