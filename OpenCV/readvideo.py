import numpy as np
import cv2

cap = cv2.VideoCapture('video.mp4')

while cap.isOpened():#cap.isOpened()，来检查是否成功初始化了
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cap.set(5, 10)
    cv2.imshow('frame',gray)
    if cv2.waitKey(0) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()