import numpy as np
import cv2

# 创建一个黑色的图片
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
cv2.line(img,(0,0),(511,511),(255,0,0),5)

#画矩形
cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)

#画圆
cv2.circle(img,(447,63), 63, (0,0,255), -1)

#画椭圆
cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)

#画多边形
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.polylines(img,[pts],True,(0,255,255))

#在图片上添加文字
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

winname = 'example'
cv2.namedWindow(winname)#新建一个显示窗口
cv2.imshow(winname, img)
cv2.waitKey(0)
cv2.destroyWindow(winname)