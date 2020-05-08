import cv2
import numpy as np

"""鼠标事件
events=[i for i in dir(cv2) if 'EVENT'in i]
print(events)
['EVENT_FLAG_ALTKEY', 'EVENT_FLAG_CTRLKEY', 'EVENT_FLAG_LBUTTON', 'EVENT_FLAG_MBUTTON',
'EVENT_FLAG_RBUTTON', 'EVENT_FLAG_SHIFTKEY', 'EVENT_LBUTTONDBLCLK', 'EVENT_LBUTTONDOWN',
'EVENT_LBUTTONUP', 'EVENT_MBUTTONDBLCLK', 'EVENT_MBUTTONDOWN', 'EVENT_MBUTTONUP', 'EVENT_MOUSEHWHEEL',
'EVENT_MOUSEMOVE', 'EVENT_MOUSEWHEEL', 'EVENT_RBUTTONDBLCLK', 'EVENT_RBUTTONDOWN', 'EVENT_RBUTTONUP']
"""

""" 
    onMouse(event, x, y, flags, param)鼠标响应函数，用于设置鼠标事件
    event：鼠标事件，可用参数对应值代替
    x：鼠标x坐标
    y：鼠标y坐标
    flags：鼠标状态，可用参数对应值代替
    param：param是用户定义的传递到setMouseCallback函数调用的参数
"""
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
"""
    cv2.setMouseCallback(windowName, onMouse, param=None)
    鼠标回调函数，用于将鼠标事件与窗口联系起来
    windowName：窗口名称
    onMouse：鼠标响应函数
    param：响应函数传递的的参数
"""
cv2.setMouseCallback('image',draw_circle)
cv2.set

while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()