import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
#img = np.zeros((300,512,3), np.uint8)
img = cv2.imread('alay.jpg',cv2.IMREAD_COLOR)

cv2.namedWindow('image',cv2.WINDOW_NORMAL)

# create trackbars for color change
#cv2.creatTrackbar(trackbarName, windowName, value, count, onChange)
#创建一个可以调整数值的轨迹条，并将轨迹条附加到指定的窗口上，它往往会和一个回调函数配合起来使用
cv2.createTrackbar('R','image',0,255,nothing)#创建滑动条
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
#switch = '0 : OFF \n1 : ON'
#cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    #获取滑动条的位置的值
    r = cv2.getTrackbarPos('R','image')#
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    #s = cv2.getTrackbarPos(switch,'image')

    # if s == 0:
    #     img[:] = 0
    # else:
    img[:] = [b,g,r]

cv2.destroyAllWindows()