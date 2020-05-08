import numpy as np
import cv2

cap = cv2.VideoCapture(0)#创建VideoCapture 对象，他的参数可以是设备的索引号，或者是一个视频文件

cap.set(3, 600)  # cap.set(propId,value) 来修改视频参数，value 就是你想要设置成的新值
cap.set(4, 400)

while True:
    ret,frame = cap.read()
    print(cap.get(4))#cap.get(propId) 来获得视频的一些参数信息
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#cv2.cvtColor将视频转为灰度图
    cv2.imshow('frame',gray)#显示视频
    if cv2.waitKey(0) & 0xff ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()