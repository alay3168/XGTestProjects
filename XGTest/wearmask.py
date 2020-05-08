import cv2
import os
import random

def add(path, filename, mode):
    img1 = cv2.imread(path)
    ############### face align
    x_min,x_max,y_min,y_max = 0,110,52,110
    ###############
    size = (x_max-x_min,y_max-y_min)
    img2 = cv2.imread('mask' + str(mode) + '.png', cv2.IMREAD_UNCHANGED) 
    img2 = cv2.resize(img2,size)
    alpha_channel = img2[:, :, 3]
    _, mask = cv2.threshold(alpha_channel, 220, 255, cv2.THRESH_BINARY)
    color = img2[:, :, :3]
    img2 = cv2.bitwise_not(cv2.bitwise_not(color, mask=mask))
    rows,cols,channels = img2.shape
    roi = img1[y_min: y_min + rows, x_min:x_min + cols]
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask)
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)
    dst = cv2.add(img1_bg,img2_fg)
    img1[y_min: y_min + rows, x_min:x_min + cols] = dst
    img_processed = filename
    cv2.imwrite(img_processed, img1)
    return img_processed


# path = 'test/grace_hopper.bmp'
# filename = 'output.bmp'
modeList = [0,1,2] # 0 or 1 or 2
inpath = 'G:\\faceImage\\test_5000\\query_5000_cropimg'
outpath = 'G:\\faceImage\\test_5000\\query_5000_cropimg\\mask'

imageNameList = os.listdir(inpath)
imputImageNameList = random.choices(imageNameList, k=3000)
num = 0
for imageName in imputImageNameList:
    mode = random.choices(modeList, k=1)
    inputName = os.path.join(inpath,imageName)
    outpuName = os.path.join(outpath,imageName)
    print(inputName)
    print(outpuName)
    print(mode[0])
    output = add(inputName, outpuName, mode[0])
    num +=1
print('num',num)

