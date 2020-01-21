#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import  QLabel,QLineEdit,QPushButton,QMainWindow,QApplication,qApp,QFileDialog
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.QtCore import QObject,QThread,pyqtSignal
from collections import defaultdict
import sys, os
from PIL import Image
import numpy as np
import cv2,json
import win32api,win32gui



class AThread(QObject):

    finished = pyqtSignal()
    update_im_rec = pyqtSignal()
    not_active = pyqtSignal()

    half_hstep=0
    half_wstep=0
    h = w = 0
    im = np.array([])
    im_rec = np.array([])
    recent_left_click=win32api.GetKeyState(0x01)
    image_cnt={}
    image_label = {}
    label = '0'
    outside_state = False

    #signal after each update of im_rec
    #used to achieve the rectangle go while the mouse moves
    def updt_im_rec(self,pt):
        self.im_rec = self.im.copy()
        try:
            cv2.rectangle(self.im_rec, pt, (pt[0] + 2*self.half_wstep, pt[1] + 2*self.half_hstep), (0,0,255), 2)
        except SystemError:
            pass

        self.update_im_rec.emit()

    def run(self):

        self.load_count()
        self.load_json('source/image_label.json')

        
        #make sure active window is correct, mouse_left_click changed, mouse within image
        while True:

            if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == 'GetSource':

                x, y = win32api.GetCursorPos()
                pixel = [y-200,x-200]
                if (0+self.half_hstep) < pixel[0] < (self.h - self.half_hstep) and (0+self.half_wstep) < pixel[1] < (self.w-self.half_wstep):
                    pt = (pixel[1]-self.half_wstep,pixel[0] - self.half_hstep)

                    self.updt_im_rec(pt)


                    current_left_click = win32api.GetKeyState(0x01)
                    if self.recent_left_click != current_left_click and current_left_click >= 0:
                        
                        self.recent_left_click = current_left_click
                        
                        
                        self.get_im(pixel)
                        print("■",end = '')

                        self.image_cnt['im_count'] += 1
                        win32api.Sleep(300)

                else:
                    if self.outside_state != True:
                        self.not_active.emit()

            else:
                self.recent_left_click = win32api.GetKeyState(0x01)
                



        self.finished.emit()


    #save image source
    def get_im(self,center):
        im = cv2.cvtColor(self.im, cv2.COLOR_BGR2RGB)
        img = im[center[0]-self.half_hstep:center[0]+self.half_hstep,center[1]-self.half_wstep:center[1]+self.half_wstep]
        s = Image.fromarray(img)
        s.save("source/im_"+str(self.image_cnt['im_count'])+".png")
        self.image_label["im_"+str(self.image_cnt['im_count'])] = self.label
        self.save_json(self.image_label,'source/image_label.json')

    #load or save json files and load image count
    def load_count(self):
            data = defaultdict(int)
            files = os.listdir('source/')
            data['im_count'] = len(files)-1-2-1
            self.image_cnt = data

    def load_json(self,path):
        try:
            with open(path, 'r') as fp:
                data = json.load(fp)
                self.image_label = data

        except json.decoder.JSONDecodeError:
            data = defaultdict(int)
            self.image_label = data

    def save_json(self,data,path):
        with open(path, 'w') as fp:
            json.dump(data, fp)

class MainWindow(QMainWindow):
    def __init__(self, val=True):
        super(MainWindow,self).__init__()
        self.hstep = 100
        self.wstep = 100
        self.file_name = ''
        self.skipx = '10'

        self.setWindowTitle('GetSource')
        self.setGeometry(200, 200, 250, 150)

        #create thread
        self.objThread = QThread()
        self.obj = AThread()
        self.obj.moveToThread(self.objThread)
        self.obj.finished.connect(self.objThread.quit)
        self.objThread.started.connect(self.obj.run)
        self.objThread.finished.connect(app.exit)
        self.objThread.start()
        self.obj.half_hstep = int(self.hstep/2)
        self.obj.half_wstep = int(self.wstep/2)
        self.obj.recent_left_click = win32api.GetKeyState(0x01)
        
        self.obj.half_hstep = int(self.hstep/2)
        self.obj.half_wstep = int(self.wstep/2)

        self.gather_wd()





    def gather_wd(self):

        #import video file
        self.file_name = QFileDialog.getOpenFileName(self, 'Open file', 
            '',"Video files (*.flv *.mp4)")[0]
        self.obj.recent_left_click = win32api.GetKeyState(0x01)

        self.vidcap = cv2.VideoCapture(self.file_name)
        
        self.obj.half_hstep = int(self.hstep/2)
        self.obj.half_wstep = int(self.wstep/2)
        
        self.count = 0
        self.success,self.obj.im = self.vidcap.read()
        self.obj.h,self.obj.w,_ = self.obj.im.shape


        #set up window displayment
        if self.obj.h > 700:
            self.setMinimumHeight(self.obj.h)
            self.setMaximumHeight(self.obj.h)    
        else:
            self.setMinimumHeight(700)
            self.setMaximumHeight(700)                

        self.setMinimumWidth(self.obj.w+120)
        self.setMaximumWidth(self.obj.w+120) 

        self.label = QLabel(self)  
        self.label.move(0,0)
        self.label.resize(self.obj.w,self.obj.h)


        lbl1 = QLabel(self)
        lbl1.setText("Height")
        lbl1.move(self.obj.w+10, 80)
        lbl1.resize(60,30) 
        lbl2 = QLabel(self)
        lbl2.setText("Width")
        lbl2.move(self.obj.w+10, 120)
        lbl2.resize(60,30) 
        lbl3 = QLabel(self)
        lbl3.setText("Label")
        lbl3.move(self.obj.w+10, 40)
        lbl3.resize(60,30) 

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(self.obj.w+10, 100)
        self.textbox1.resize(60,30)
        self.textbox1.setText(str(self.hstep))
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(self.obj.w+10, 140)
        self.textbox2.resize(60,30) 
        self.textbox2.setText(str(self.wstep))

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(self.obj.w+10, 60)
        self.textbox3.resize(60,30) 
        self.textbox3.setText(self.obj.label)

        self.textbox4 = QLineEdit(self)
        self.textbox4.move(self.obj.w+5, 600)
        self.textbox4.resize(100,30) 
        self.textbox4.setText(self.skipx)


        btn4 = QPushButton("Next", self)
        btn4.move(self.obj.w+5, 180)
        btn4.resize(100,400)
        btn4.clicked.connect(self.passing)
        btn5 = QPushButton("Skip", self)
        btn5.move(self.obj.w+5, 640)
        btn5.resize(100,50)
        btn5.clicked.connect(self.passing_x)
        btn6 = QPushButton("Update", self)
        btn6.move(self.obj.w+70, 60)
        btn6.resize(42,110)
        btn6.clicked.connect(self.update)

        self.textbox = QLineEdit(self)
        self.textbox.move(self.obj.w+10,10)
        self.textbox.resize(60,30)
        self.textbox.setDisabled(True)

        self.obj.update_im_rec.connect(self.renew_im)
        self.obj.not_active.connect(self.not_active_)

        self.show()


        #set pixmap to label
        if self.success:

            
            pixmap = self.create_QPixmap()
            self.label.setPixmap(pixmap)
            
            self.textbox.setText(str(self.obj.image_cnt['im_count']))

        else:
            print("No Video Input or Video Ended...")
            sys.exit(0)
            return -1

        self.obj.recent_left_click = win32api.GetKeyState(0x01)

        #self.textbox.setDisabled()

    #update the label,hstep and wstep
    def update(self):
        self.hstep = int(self.textbox1.text())
        self.wstep = int(self.textbox2.text())
        self.obj.half_hstep = int(self.hstep/2)
        self.obj.half_wstep = int(self.wstep/2)
        self.obj.label = self.textbox3.text()
        self.obj.recent_left_click = win32api.GetKeyState(0x01)

    # respond if window is not active
    def not_active_(self):
        pixmap = self.create_QPixmap()
        self.label.setPixmap(pixmap)   
        self.obj.outside_state = True    

    # if window is in active and mouse is within the area of image
    def renew_im(self):

        pixmap = self.create_QPixmap2()
        self.label.setPixmap(pixmap)
        self.textbox.setText(str(self.obj.image_cnt['im_count']))
        self.obj.outside_state = False

    #short-cut functions for setting up pixelmap
    def create_QPixmap2(self):
        im = cv2.cvtColor(self.obj.im_rec, cv2.COLOR_BGR2RGB)
        image = np.uint8(im).copy()
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def create_QPixmap(self):
        
        im = cv2.cvtColor(self.obj.im, cv2.COLOR_BGR2RGB)

        image = np.uint8(im).copy()
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        return pixmap


    # skip x images within the video
    def passing_x(self):

        cnt = int(self.textbox4.text())
        while cnt > 0:
            if self.success:
                self.success,self.obj.im = self.vidcap.read()   
                cnt -= 1

            else:
                print("No Video Input or Video Ended...")
                sys.exit(0)
                return -1

        pixmap = self.create_QPixmap()
        self.label.setPixmap(pixmap)
        self.textbox.setText(str(self.obj.image_cnt['im_count']))
        self.obj.recent_left_click = win32api.GetKeyState(0x01)


    #next image in video
    def passing(self):

        if self.success:

            self.success,self.obj.im = self.vidcap.read() 
            pixmap = self.create_QPixmap()
            self.label.setPixmap(pixmap)
            self.textbox.setText(str(self.obj.image_cnt['im_count']))
            self.obj.recent_left_click = win32api.GetKeyState(0x01)

        else:
            print("No Video Input or Video Ended...")
            sys.exit(0)
            return -1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

