# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 17:45:11 2019

@author: Administrator
"""

import sys
import os
import time
import datetime
import json
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
from pprint import pprint
from datetime import datetime

from video_show.video_show_ui import  Ui_video_show  # 导入创建的GUI类


def cv_imread(file_path = ""):
    file_path_gbk = file_path.encode('gbk')        # unicode转gbk，字符串变为字节数组
    img_mat = cv2.imread(file_path_gbk.decode())  # 字节数组直接转字符串，不解码
    return img_mat

def cv_imdraw_fixed(img, frame_id):
    draw_text = "FrameID:{}".format(frame_id)
    cv2.putText(img,draw_text,(10,50),cv2.FONT_HERSHEY_PLAIN ,2,(0,255,0),2)



def cv_imdraw(img, width, height, face_data):
    colorlist = [ (128,128,128), (255,140,0), (255,255,0), (0,255,0), (47,79,79), (0,0,255), (128,0,128), (0,0,0), (128,128,128),(255,0,0)]
    b,g,r = (0,255,0)
    if face_data:
        #print(face_data['RealFid'], face_data['FaceCount'])
        for val in face_data['astFaceInfo']:
            left = int(val['Rect']['Left'] * (width/face_data['Width']))
            top = int(val['Rect']['Top'] * (height/face_data['Height']))
            right = int(val['Rect']['Right'] * (width/face_data['Width']))
            bottom = int(val['Rect']['Bottom'] * (height/face_data['Height']))
                
            if float(val['W']) > 2.0:
                b,g,r = (0,255,0)       #绿色
            else:
                b,g,r = (0,0,255)       #红色
            
            cv2.rectangle(img,(left,top),(right,bottom),(b,g,r),2) 
            cv2.rectangle(img,(left+10,top+10),(right-10,bottom-10),colorlist[int(val['FaceType'])],2)

            draw_text_x = right
            draw_text_y = top
            draw_text = "t:{}".format(val['TraceID'])
            cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                            cv2.FONT_HERSHEY_PLAIN ,1.5,colorlist[int(val['FaceType'])],2)
            draw_text_y = draw_text_y + 20
            draw_text = "c:{}".format(val['Confidenc'])
            cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                            cv2.FONT_HERSHEY_PLAIN ,1.5,colorlist[int(val['FaceType'])],2)
            draw_text_y = draw_text_y + 20
            draw_text = "t:{}".format(val['FaceType'])
            cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                            cv2.FONT_HERSHEY_PLAIN ,1.5,colorlist[int(val['FaceType'])],2)
            draw_text_y = draw_text_y + 20
            draw_text = "rpy:{} {} {}".format(val['3DPose']['Roll'], 
                val['3DPose']['Pitch'], val['3DPose']['Yaw'])
            cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                            cv2.FONT_HERSHEY_PLAIN ,1.5,colorlist[int(val['FaceType'])],2)
            draw_text_y = draw_text_y + 20
            draw_text = "b:{}".format(val['Blur'])
            cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                            cv2.FONT_HERSHEY_PLAIN ,1.5,colorlist[int(val['FaceType'])],2)
            draw_text_y = draw_text_y + 20
            draw_text = "w:{}".format(val['W'])
            cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                            cv2.FONT_HERSHEY_PLAIN ,1.5,colorlist[int(val['FaceType'])],2)
            draw_text_y = draw_text_y + 20
            #print("draw_text:{}".format(draw_text))
'''
    if face_data:
        #print("face_data.len=",len(face_data))
        #pprint(face_data)
        for val in face_data:
            
            #if val['frame_id'] == 30:
            #    pprint(val)
            
            left = int(val['left'] * (width/val['width']))
            top = int(val['top'] * (height/val['height']))
            right = int(val['right'] * (width/val['width']))
            bottom = int(val['bottom'] * (height/val['height']))
            
            if val['type'] is 0:
                b,g,r = (0,255,0)
            else:
                b,g,r = (0,0,255)
            if 'color' in val:
                draw_color = val['color']
                b = draw_color['b']
                g = draw_color['g']
                r = draw_color['r']
            
            cv2.rectangle(img,(left,top),(right,bottom),(b,g,r),2) 
    
            draw_text_x = right
            draw_text_y = top
            
# =============================================================================
#             #绘制frame_id
#             draw_text = "frame:{}".format(val['frame_id'])
#             cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
#                             cv2.FONT_HERSHEY_PLAIN ,1.5,(0,255,0),2)
#             draw_text_y = draw_text_y + 20
#             #print("draw_text:{}".format(draw_text))
# =============================================================================
                      
            #绘制track_id-image_count
            draw_text = "track:{}-{}".format(val['track_id'], val['image_cnt'])
            cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                            cv2.FONT_HERSHEY_PLAIN ,1.5,(0,255,0),2)
            draw_text_y = draw_text_y + 20
            #print("draw_text:{}".format(draw_text))
            
            #绘制info
            if 'info' in val:
                for skey,sval in val['info'].items():
                    if type(sval) is float:
                        draw_text = "{}:{:.2f}".format(skey, sval)
                    else:
                        draw_text = "{}:{}".format(skey, sval)
                    cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                                cv2.FONT_HERSHEY_PLAIN ,1.5,(0,255,0),2)
                    draw_text_y = draw_text_y + 20
                    #print("draw_text:{}".format(draw_text))
                
            #绘制fixed_info
            if 'fixed_info' in val:
                #pprint(face_data)
                for skey,sval in val['fixed_info'].items():
                    #print("draw:{}-{}".format(draw_text_x,draw_text_y))
                    if type(sval) is float:
                        draw_text = "{}:{:.2f}".format(skey, sval)
                    else:
                        draw_text = "{}:{}".format(skey, sval)
                    cv2.putText(img,draw_text,(draw_text_x,draw_text_y),
                                cv2.FONT_HERSHEY_PLAIN ,1.5,(0,255,0),2)
                    draw_text_y = draw_text_y + 20
                    #print("draw_text:{}".format(draw_text))
'''
def cv_jsonload(file_path = ""):
    
    #line_count = 0
    width = 1920
    height = 1080
    detect_list = []
    dict_hash = {}
    extra_info_list = {}
    extra_count_list = {}  #主要记录推图个数
    
    with open(file_path) as load_f:
        while True:
            line = load_f.readline()
            if line:
                load_dict = json.loads(line)
                ret = dict_hash.get(load_dict['RealFid'])
                if ret is None:
                    dict_hash[load_dict['RealFid']] = load_dict
                else:
                    break
                
            else:
                break
    detect_list.append(dict_hash)
    return detect_list

class communicate(QObject):

    signal = pyqtSignal(int, str)


class video_show_timer(QThread):
    
    TIME_FPS_SLEEP = 0
    TIME_NO_SLEEP = 1
    
    sleep_flag = TIME_FPS_SLEEP
    
    def __init__(self, fps=25):
        QThread.__init__(self)
        self.stopped = False
        self.fps = fps
        self.time_signal = communicate()
        self.mutex = QMutex()
        
    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            
            #begin = (int(round(time.time() * 1000))) 
            self.time_signal.signal.emit(0,"1")
            #end = (int(round(time.time() * 1000))) 
            #print ('fps'+ str(self.fps))
            if self.sleep_flag is video_show_timer.TIME_FPS_SLEEP:
                time.sleep(1 / self.fps)
                #time.sleep(0.020)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.fps = fps
        self.sleep_flag = video_show_timer.TIME_FPS_SLEEP
    
    def set_no_sleep(self):
        self.sleep_flag = video_show_timer.TIME_NO_SLEEP
        
class video_encode_timer(QThread):
    
    frame_id = 1
    
    def __init__(self):
        QThread.__init__(self)
        self.stopped = False
        self.video_capture = cv2.VideoCapture()
        self.time_signal = communicate()
        self.mutex = QMutex()
        
    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            if self.video_capture.isOpened():
                success, frame = self.video_capture.read()
                if success:
                    height, width = frame.shape[:2]
                    #cv_imdraw_fixed(frame, self.frame_id)
                    #if self.frame_id in self.detect_list:
                        #cv_imdraw(frame,width,height,self.detect_list[self.frame_id])
                    if self.encode_type is video_window.ENCODE_TYPE_VIDEO:
                        self.encode_out_file.write(frame)
                    elif self.encode_type is video_window.ENCODE_TYPE_PIC:
                        new_path = os.path.join(self.encode_file_path,"frame_{}.jpg".format(str(self.frame_id)))
                        cv2.imencode('.jpg', frame)[1].tofile(new_path)
                    #print("video_show:frame_id={},image_size={}:{}".format(
                                    #self.frame_id,width,height))
                    self.frame_id = self.frame_id + 1
                    self.time_signal.signal.emit(self.frame_id,'encoding')
                    
                else:
                    print("encode_timer:read failed, no frame data")
                    success, frame = self.video_capture.read()
                    if not success:
                        print("encode_timer:play finished")  # 判断本地文件播放完毕
                        self.encode_finish()
                        self.time_signal.signal.emit(self.frame_id,'finished')
                    return
            else:
                self.encode_finish()
                self.time_signal.signal.emit(self.frame_id,'finished')
                print("encode_timer:open file or capturing device error, init again")
                
    def encode_start(self):
        self.video_capture.open(self.file_name)
        self.frame_rate = int(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        if self.encode_type is video_window.ENCODE_TYPE_VIDEO:
            fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
            self.encode_file_name = os.path.join(self.encode_file_path,
                                "{}_out.avi".format(os.path.basename(self.file_name)))
            self.encode_out_file = cv2.VideoWriter(self.encode_file_name,fourcc,
                                               self.frame_rate,(self.frame_width,self.frame_height))
            
            print("encode_start_video:file={}".format(self.encode_file_name))
        else:
            print("encode_start_pic:path={}".format(self.encode_file_path))
        
    def encode_finish(self):
        
        self.video_capture.release()
        if self.encode_type is video_window.ENCODE_TYPE_VIDEO:
            self.encode_out_file.release()
            print("encode_finish_video:file={}".format(self.encode_file_name))
        else:
            print("encode_finish_pic:path={}".format(self.encode_file_path))
                
    def set_param(self,file_name,detect_list,encode_type,encode_file_path):
        with QMutexLocker(self.mutex):
            self.stopped = False
            self.frame_id = 1
            self.file_name = file_name
            self.detect_list = detect_list
            self.encode_type = encode_type
            self.encode_file_path = encode_file_path
            self.encode_start()
            

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True
            self.video_capture.release()
        
        
class video_window(QtWidgets.QWidget, Ui_video_show):
    
    VIDEO_STATUS_IDLE = 0
    VIDEO_STATUS_OPEN = 1
    VIDEO_STATUS_PLAY = 2
    VIDEO_STATUS_PAUSE = 3
    VIDEO_STATUS_STEP = 4
    VIDEO_STATUS_ENCODE = 5
    VIDEO_STATUS_FINISH = 6
    
    ENCODE_TYPE_VIDEO = 0
    ENCODE_TYPE_PIC = 1
    
    #原视频文件信息
    frame_id = 1
    frame_total_id = 10000
    frame_width = 1920
    frame_height = 1080
    frame_rate = 25
    frame_rate_play = 25
    
    #选择路径
    cur_input_pwd = "."
    cur_output_pwd = "."
    
    #配置文件信息
    draw_flag = 0
    detect_list = []
    
    #转码相关信息
    encode_flag = 0
    encode_type = ENCODE_TYPE_VIDEO
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.open_button.clicked.connect(self.open_button_func)   # 建立button的槽连接事件  
        self.play_button.clicked.connect(self.play_button_func)   # 建立button的槽连接事件                                                      
        self.open_cfg_button.clicked.connect(self.open_cfg_button_func)   # 建立button的槽连接事件      
        self.encode_video_button.clicked.connect(self.prev_button_func)   # 建立button的槽连接事件    
        self.encode_jpg_button.clicked.connect(self.next_button_func)   # 建立button的槽连接事件
        self.set_fps_button.clicked.connect(self.set_fps_button_func)   # 建立button的槽连接事件
        #self.next_button.clicked.connect(self.next_button_func)   # 建立button的槽连接事件  
        #self.prev_button.clicked.connect(self.prev_button_func)   # 建立button的槽连接事件  
        #self.skip_button.clicked.connect(self.skip_button_func)   # 建立button的槽连接事件  
        
        #self.show_label.setFrameShadow(QtWidgets.QFrame.Raised)
        
        # setting main window geometry
        desktop_geometry = QtWidgets.QApplication.desktop()  # 获取屏幕大小
        main_window_width = desktop_geometry.width()  # 屏幕的宽
        main_window_height = desktop_geometry.height()  # 屏幕的高
        rect = self.geometry()  # 获取窗口界面大小
        window_width = rect.width()  # 窗口界面的宽
        window_height = rect.height()  # 窗口界面的高
        x = (main_window_width - window_width) / 2  # 计算窗口左上角点横坐标
        y = (main_window_height - window_height) / 2 # 计算窗口左上角点纵坐标
        #self.setGeometry(x, y, window_width, window_height)  # 设置窗口界面在屏幕上的位置        
        print("init_window: desktop={}:{}, window={}:{}".format(main_window_width,
              main_window_height, window_width, window_height))
        
        # video_timer 设置
        self.video_timer = video_show_timer()
        self.video_timer.time_signal.signal[int,str].connect(self.video_show_image)
        
        # encode_timer 设置
        self.encode_timer = video_encode_timer()
        self.encode_timer.time_signal.signal[int,str].connect(self.video_encode_image)
        
        # video 初始设置
        self.playCapture = cv2.VideoCapture()
        
    def get_input_file(self):
        file_name,file_type = QFileDialog.getOpenFileName(self,'选择文件',self.cur_input_pwd,'files(*.*)')
        self.cur_input_pwd = os.path.dirname(file_name)
        return file_name,file_type
    
    def get_input_path(self):
        path = QFileDialog.getExistingDirectory(self,'选择打开路径',self.cur_input_pwd)
        self.cur_input_pwd = path
        return path
        
    def get_output_file(self):
        file_name,file_type = QFileDialog.getOpenFileName(self,'保存文件',self.cur_output_pwd,'files(*.*)')
        self.cur_output_pwd = os.path.dirname(file_name)    
        return file_name,file_type
        
    def get_output_path(self):
        path = QFileDialog.getExistingDirectory(self,'选择保存路径',self.cur_output_pwd)
        self.cur_output_pwd = path
        return path
        
    def video_status_updata(self):
        
        if self.status is video_window.VIDEO_STATUS_IDLE:
            self.status_label.setText("{}".format("idle"))
        elif self.status is video_window.VIDEO_STATUS_OPEN:
            self.status_label.setText("{},fps:{}".format("open",self.frame_rate_play))
        elif self.status is video_window.VIDEO_STATUS_PLAY:
            self.status_label.setText("{},fps:{}".format("playing",self.frame_rate_play))
        elif self.status is video_window.VIDEO_STATUS_PAUSE:
            self.status_label.setText("{},fps:{}".format("pause",self.frame_rate_play))
        elif self.status is video_window.VIDEO_STATUS_STEP:
            self.status_label.setText("{},fps:{}".format("steping",self.frame_rate_play))
        elif self.status is video_window.VIDEO_STATUS_ENCODE:
            self.status_label.setText("{}".format("encoding"))
        elif self.status is video_window.VIDEO_STATUS_FINISH:
            self.status_label.setText("{}".format("finished"))
        
    def video_reset(self):
        self.frame_id = 1
        self.video_timer.stop()
        self.playCapture.release()
        self.status = video_window.VIDEO_STATUS_IDLE
        self.video_status_updata()
        
    def video_finish(self):
        self.frame_id = 1
        self.video_timer.stop()
        self.playCapture.release()
        self.status = video_window.VIDEO_STATUS_FINISH
        self.video_status_updata()
        self.play_button.setText("开始")
        self.message_box_show("播放结束")

    def video_open(self):
        self.playCapture.open(self.openfile_name)
        self.frame_total_id = self.playCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_rate = self.playCapture.get(cv2.CAP_PROP_FPS)
        self.frame_width = self.playCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.playCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_rate_play = self.frame_rate
        self.status = video_window.VIDEO_STATUS_OPEN
        self.video_status_updata()
        self.play_button.setText("开始")
        
        print("init_video_file: size={}:{},fps={},total={}".format(self.frame_width,
              self.frame_height, self.frame_rate,self.frame_total_id))
    
    #reopen 不修改播放帧率
    def video_reopen(self):
        self.playCapture.open(self.openfile_name)
        self.frame_total_id = self.playCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_rate = self.playCapture.get(cv2.CAP_PROP_FPS)
        self.frame_width = self.playCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.playCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.status = video_window.VIDEO_STATUS_OPEN
        self.video_status_updata()
        self.play_button.setText("开始")
        
        print("init_video_file: size={}:{},fps={},total={}".format(self.frame_width,
              self.frame_height, self.frame_rate,self.frame_total_id))
        
    def video_encode_image(self,frame_id,status):
        self.display_label.setText("{}:{}".format("display",frame_id))
        self.status_label.setText(status)
        if status == "finished":
            self.message_box_show("转码结束")
    def video_show_image1(self):
        if self.playCapture.isOpened():
            #begin = (int(round(time.time() * 1000))) 
            success, frame = self.playCapture.read() #frame bgr24
        else:
            print("open file or capturing device error, init again")
            self.video_finish()

    def video_show_image(self):
        if self.playCapture.isOpened():
            #begin = (int(round(time.time() * 1000))) 
            success, frame = self.playCapture.read() #frame bgr24
            if success:
                height, width = frame.shape[:2]
                yuv420p = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #yuv420p.tofile('yuv420p.yuv')
                mark = [1,0,1,0,1,0,1,0]
                flg = 0
                realframeid = 0
                for i in range(len(yuv420p[0,:8])):
                    if(mark[i] != (yuv420p[0,:8][i] > 0x80)):
                        flg = 1
                        break
                for i in range(len(yuv420p[0,24:32])):
                    if(mark[i] != (yuv420p[0,:8][i] > 0x80)):
                        flg = 1
                        break
                if not flg:
                    for i in range(16):
                        m = 0
                        if yuv420p[0, i+8] > 0x80:
                            m=1
                        else:
                            m=0
                        realframeid = realframeid | (m << (16-(i+1)))
                    #print(realframeid)
                    
                    if len(self.detect_list) > 0 and realframeid in  self.detect_list[0]:
                        info = self.detect_list[0][realframeid]
                        if self.draw_flag and realframeid in self.detect_list[0]:
                            cv_imdraw(frame,width,height,info)

                cv_imdraw_fixed(frame, realframeid)
                if frame.ndim == 3:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                lable_size = self.show_label.geometry()
                #label的大小需要主动减去2,因为包含Frame Box
                if lable_size.width() < width and lable_size.height() < height:                       
                    p = temp_image.scaled(lable_size.width()-2,lable_size.height()-2,
                                          Qt.KeepAspectRatio)
                    temp_pixmap = QPixmap.fromImage(p)
                    self.show_label.setPixmap(temp_pixmap)
                    #print("video_show:frame_id={},image_size={}:{},pos={}".format(
                            #self.frame_id,temp_pixmap.width(),temp_pixmap.height(),
                            #self.playCapture.get(cv2.CAP_PROP_POS_FRAMES)))
                else:
                    self.show_label.setPixmap(temp_image)
                    #print("video_show:frame_id={},image_size={}:{}".format(
                       #     self.frame_id,temp_image.width(),temp_image.height()))
                #self.display_label.setText("{}:{}/{}".format("display",self.frame_id,self.frame_total_id))
                self.display_label.setText("{}:{}".format("display",realframeid))
                #self.frame_id = self.frame_id + 1
                
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success:
                    print("play finished")  # 判断本地文件播放完毕
                    self.video_finish()
                return
            #end = (int(round(time.time() * 1000))) 
            #print (end-begin)
        else:
            print("open file or capturing device error, init again")
            self.video_finish()
            

    def video_switch_to_play(self):
        self.video_timer.start()
        self.video_timer.set_fps(self.frame_rate_play)
        self.play_button.setText("暂停")
        self.status =  video_window.VIDEO_STATUS_PLAY
        self.video_status_updata()
        
    def video_switch_to_pause(self):
        self.video_timer.stop()
        self.play_button.setText("开始")
        self.status =  video_window.VIDEO_STATUS_PAUSE
        self.video_status_updata()
        
    def video_switch_to_encode(self):
        self.encode_timer.set_param(self.openfile_name,self.detect_list,
                                self.encode_type,self.encode_file_path)
        self.encode_timer.start()
        self.status =  video_window.VIDEO_STATUS_ENCODE
        self.video_status_updata()
                
    def video_play_switch(self):
        if self.openfile_name == "" or self.openfile_name is None:
            self.message_box_show("请选择视频源文件")
            return
        if self.status is video_window.VIDEO_STATUS_IDLE:
            self.video_open()
            self.video_switch_to_play()
            print("video_play_switch:idle-play")
        elif self.status is video_window.VIDEO_STATUS_FINISH:
            self.video_reopen()
            self.video_switch_to_play()
            print("video_play_switch:finish-play")
        elif self.status is video_window.VIDEO_STATUS_OPEN:
            self.video_switch_to_play()
            print("video_play_switch:open-play")
        elif self.status is video_window.VIDEO_STATUS_PLAY:
            self.video_switch_to_pause()
            print("video_play_switch:play-pause")
        elif self.status is video_window.VIDEO_STATUS_PAUSE:
            self.video_switch_to_play()
            print("video_play_switch:pause-play")
        elif self.status is video_window.VIDEO_STATUS_STEP:
            self.video_switch_to_play()
            print("video_play_switch:step-play")
            
    def video_step_switch(self):
        if self.openfile_name == "" or self.openfile_name is None:
            self.message_box_show("请选择视频源文件")
            return False
        if self.status is video_window.VIDEO_STATUS_IDLE \
            or self.status is video_window.VIDEO_STATUS_FINISH:
            
            self.video_open()
            self.status =  video_window.VIDEO_STATUS_STEP
            self.video_status_updata()
            print("video_step_switch:idle/finish-step")
            return True
        elif self.status is video_window.VIDEO_STATUS_OPEN:
            self.play_button.setText("开始")
            self.status =  video_window.VIDEO_STATUS_STEP
            self.video_status_updata()
            print("video_step_switch:open-step")
            return True
        elif self.status is video_window.VIDEO_STATUS_PLAY:
            self.video_timer.stop()
            self.play_button.setText("开始")
            self.status =  video_window.VIDEO_STATUS_STEP
            self.video_status_updata()
            print("video_step_switch:play-step")
            return True
        elif self.status is video_window.VIDEO_STATUS_PAUSE:
            self.video_status_updata()
            print("video_step_switch:pause-step")
            return True
        
    def video_encode_switch(self):
        if self.openfile_name == "" or self.openfile_name is None:
            self.message_box_show("请选择视频源文件")
            return False
        if self.encode_file_path == "" or self.encode_file_path is None:
            self.message_box_show("请选择转码存储路径")
            return False
        if self.status is video_window.VIDEO_STATUS_IDLE \
            or self.status is video_window.VIDEO_STATUS_FINISH \
            or self.status is video_window.VIDEO_STATUS_OPEN:                
            self.video_switch_to_encode()
            print("video_step_switch:idle/open/finish-encode")
            return True
        elif self.status is video_window.VIDEO_STATUS_PLAY \
            or self.status is video_window.VIDEO_STATUS_PAUSE \
            or self.status is video_window.VIDEO_STATUS_STEP:
                
            self.video_finish()
            self.video_switch_to_encode()
            print("video_step_switch:play-encode")
            return True
        
    def message_box_show(self, text):
        QMessageBox.information(self,"Information",self.tr(text))
            
    def open_button_func(self):
        self.openfile_name, self.openfile_type = self.get_input_file()
        if self.openfile_name:
            self.video_reset()
            self.video_open()
            self.filename_label.setText(self.openfile_name)
            print("open_button_func:file={}".format(self.openfile_name))
        
    def open_cfg_button_func(self):
        self.cfgfile_name, self.cfgfile_type = self.get_input_file()
        if self.cfgfile_name:
            self.detect_list = cv_jsonload(self.cfgfile_name)
            self.draw_flag = 1        
            print("open_cfg_button_func:file={}".format(self.cfgfile_name))
        
    def encode_video_button_func(self):
        self.encode_file_path =  self.get_output_path()
        if self.encode_file_path:
            self.encode_flag = 1
            self.encode_type = video_window.ENCODE_TYPE_VIDEO
            self.video_encode_switch()

        #self.video_switch_to_encode()
        #fourcc = cv2.VideoWriter_fourcc('X','2','6','4')
        #encode_file_name = self.encode_file_path + 'output'+ datetime.now().strftime("%Y%m%d_%H%M%S")+'.264'
        
        #encode_file_name = self.encode_file_path + os.path.basename(self.openfile_name)+'_out.264'
        #self.encode_out_file = cv2.VideoWriter(encode_file_name,fourcc,
                                               #self.frame_rate,(self.frame_width,self.frame_height))
        #print("encode_video_button_func:file={}".format(encode_file_name))
        
        
    def encode_jpg_button_func(self):
        self.encode_file_path =  self.get_output_path()
        if self.encode_file_path:
            self.encode_flag = 1
            self.encode_type = video_window.ENCODE_TYPE_PIC
            self.video_encode_switch()
  
            print("encode_jpg_button_func:path={}".format(self.encode_file_path))
        
    def play_button_func(self):
        # self.cfgfile_name = 'E:\\H264\\video_show\\result_0.json'
        # self.detect_list = cv_jsonload(self.cfgfile_name)
        # self.draw_flag = 1  

        # self.openfile_name = 'E:\\H264\\3m_258face_proc.264'
        # self.video_reset()
        # self.video_open()
        # self.filename_label.setText(self.openfile_name)
        # print("open_button_func:file={}".format(self.openfile_name))

        self.video_play_switch()
        print("play_button_func:file={}".format(self.openfile_name))
        
        #Im = cv_imread(self.openfile_name) #通过Opencv读入一张图片
        #image_height, image_width, image_depth = Im.shape  # 获取图像的高，宽以及深度。
        #QIm = cv2.cvtColor(Im, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        #QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
        #             image_width * image_depth,
        #             QImage.Format_RGB888)
        #self.show_label.setPixmap(QPixmap.fromImage(QIm))  # 将QImage显示在之前创建的QLabel控件中
        #self.show_label.setScaledContents(True)
        
    def set_fps_button_func(self):
        fps = self.set_fps_line.text()
        if fps:
            self.frame_rate_play = int(fps)
            print("set_fps_button_func:fps={}".format(self.frame_rate_play))
            #self.video_timer.start()
            self.video_timer.set_fps(self.frame_rate_play)
            self.video_status_updata()
            self.message_box_show("帧率设置为：{}".format(self.frame_rate_play))
 
    def next_button_func(self):
        self.video_step_switch()
        #self.frame_id = self.frame_id  #将视频ID默认指向下一帧
        #print("next_button_func:frame_id={}".format(self.frame_id))
        #frameid = self.playCapture.get(cv2.CAP_PROP_POS_FRAMES)
        #self.playCapture.set(cv2.CAP_PROP_POS_FRAMES, frameid+1)
        #frameid = self.playCapture.get(cv2.CAP_PROP_POS_FRAMES)
        print(self.playCapture.get(cv2.CAP_PROP_POS_FRAMES))
        self.video_show_image()
        
    def prev_button_func(self):
        # self.video_step_switch()
        # frameid = self.playCapture.get(cv2.CAP_PROP_POS_FRAMES)
        # if frameid > 1:
        #     self.playCapture.set(cv2.CAP_PROP_POS_FRAMES, frameid-1)
        #     self.video_show_image()

        self.video_step_switch()
        loop = 0
        while(loop < 8300):
            loop += 1
            self.video_show_image1()

        #if self.frame_id > 1:
        #    self.frame_id = self.frame_id-2  #将视频ID默认指向下一帧
        #    print("prev_button_func:frame_id={}".format(self.frame_id))
        #    self.playCapture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_id)
        #    self.video_show_image()
            
    def skip_button_func(self):
        self.video_step_switch()
        skip_frame_id = self.skip_line.text()
        if skip_frame_id:
            self.frame_id = int(skip_frame_id)
            print("skip_button_func:frame_id={}".format(self.frame_id))
            self.playCapture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_id)
            self.video_show_image()
        
if __name__ == "__main__":
    

    app = QtWidgets.QApplication(sys.argv)
    ui = video_window()
    ui.show()
    sys.exit(app.exec_())
