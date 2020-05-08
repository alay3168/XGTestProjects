import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480),1)##创建一个 VideoWriter 的对象，确定一个输出文件的名字。接下来指定 FourCC 编码，播放频率和帧的大小也都需要确定。最后一个是 isColor 标签。如果是 True，每一帧就是彩色图，否则就是灰度图

while cap.isOpened():
    ret,frame = cap.read()
    if ret == True:
        frame =cv2.flip(frame,0)#图像翻转
        out.write(frame)#写入图像
        cv2.imshow('frame',frame)#显示输出的图像
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
cap.release()
out.release()
cv2.destroyAllWindows()