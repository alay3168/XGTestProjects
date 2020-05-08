import cv2
import os

face_patterns = cv2.CascadeClassifier('D:\Program Files\Python35\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

sample_image = cv2.imread('face.jpg')

faces = face_patterns.detectMultiScale(sample_image,scaleFactor=1.1,minNeighbors=5,minSize=(100,100))
for (x,y,w,h) in faces:
    cv2.rectangle(sample_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imwrite('detected.png', sample_image);

