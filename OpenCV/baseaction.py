import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("alay.jpg",cv2.IMREAD_COLOR)#读取图片,第二个参数是要告诉函数应该如何读取这幅图片,cv2.IMREAD_COLOR，cv2.IMREAD_GRAYSCALE，cv2.IMREAD_UNCHANGED
print(img)

#cv2.imshow('alay',img)#显示图片
#cv2.waitKey(0)#等待键盘输入，如果我们设置这个函数的参数为 0，那它将会无限期的等待键盘输入
#cv2.destroyAllWindows()#可以轻易删除任何我们建立的窗口
#cv2.destroyWindow('alay')删除特定的窗口

cv2.imwrite('messigray.png',img)#保存图片，第一个参数图像名称，第二个参数是要保存的参数

meimg = cv2.imread('messigray.png',cv2.IMREAD_UNCHANGED)

plt.imshow(meimg,cmap='gray',interpolation='bicubic')
plt.xticks([])
plt.yticks([])
plt.show()