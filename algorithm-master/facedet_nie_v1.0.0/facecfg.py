
facecfg = dict(
    facedet_v=dict(
        deploy='facedet_nie_v1.0.0/deploy_inference.prototxt',
        model='facedet_nie_v1.0.0/caffe_inference.caffemodel'
    ),
    img_preprocess = dict(
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        shape=(320,320)
    ),
    anchor = dict(
        scale=[2,2.82842],
        ratio=[1.0,1.5],
        stride=[8,16,32]
    ),
    process=dict(
        nms_thre=0.3,
        score=0.3
    ),
    test_imglist="./data/puppy_imglist",
    vis_detresult=True
)
