# Algorithm

##  **Introduce**

test code for facedet_nie_* caffemodel 

please read facedet_*/facecfg.py

**facedet_v**: facedet_version

**img_preprocess**： img > reshape > rgb > -mean/std 

**anchor** : for anchor generator 

**process** : for result process 

**test_imglist** : testimg_path 

**vis_detresult** : vis result or not

## test_model

测试环境：采用caffe框架， caffe安装参考./caffe/README.md 编译环境建议使用ubuntu14.04,16.04，python2.7

测试语言： python2.7 与caffe编译一致

./demo.sh facedet_nie_v1.0.0 


