#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import  *
from PyQt5.QtGui import QIcon, QPixmap,QImage
from collections import defaultdict
import json, sys
from PIL import Image
import numpy as np
import cv2


class MainWindow(QMainWindow):
    def __init__(self, val=True):
        super(MainWindow,self).__init__()
        self.setWindowTitle('GetSource')
        self.setGeometry(1000, 500, 250, 150)
        
        if val:
            self.InitWindow()
        else:

            self.load_count()
            self.load_json('source/image_label.json')

            self.gather_wd()

            


    def InitWindow(self):

        self.setMinimumHeight(150)
        self.setMinimumWidth(250)
        self.setMaximumHeight(150)
        self.setMaximumWidth(250)

        lbl1 = QLabel(self)
        lbl1.setText("Height")
        lbl1.move(15, 20)
        lbl2 = QLabel(self)
        lbl2.setText("Weight")
        lbl2.move(135, 20)
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(15, 40)
        self.textbox1.resize(100,30)
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(135, 40)
        self.textbox2.resize(100,30)      
        btn1 = QPushButton("Run", self)
        btn1.move(15, 80)
        btn2 = QPushButton("Exit", self)
        btn2.move(135, 80)
        btn1.clicked.connect(self.c_open_new)
        btn2.clicked.connect(qApp.quit)
        self.show()

    def c_open_new(self): 
        try:
            self.hstep = int(self.textbox1.text())
            self.wstep = int(self.textbox2.text())
        except ValueError:
            print("Not Numeric Values")
            qApp.quit()
            return -1

        self.close()
        self.__init__(False)



    def create_QPixmap(self):
        self.im = cv2.cvtColor(self.im, cv2.COLOR_BGR2RGB)
        image = np.uint8(self.im).copy()
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def close_wd(self):
        qApp.quit
        return -1

    def gather_wd(self):

        self.vidcap = cv2.VideoCapture('sample.flv')
        self.count = 0
        self.success,self.image = self.vidcap.read()

        if self.hstep < 150:
            self.setMinimumHeight(150)
            self.setMaximumHeight(150)
        else:
            self.setMinimumHeight(self.hstep)
            self.setMaximumHeight(self.hstep)           

        self.setMinimumWidth(self.wstep+120)
        self.setMaximumWidth(self.wstep+120) 

        self.label = QLabel(self)  
        self.label.move(0,0)
        self.label.resize(self.wstep,self.hstep)
        btn1 = QPushButton("Monster", self)
        btn2 = QPushButton("Other", self)
        btn1.move(self.wstep+5, 40)
        btn2.move(self.wstep+5, 80)
        btn1.clicked.connect(self.save_img)
        btn2.clicked.connect(self.save_img2)
        btn1 = QPushButton("Skip", self)
        btn1.move(self.wstep+5, 120)
        btn1.clicked.connect(self.passing)


        self.textbox = QLineEdit(self)
        self.textbox.move(self.wstep+5,10)
        self.textbox.resize(60,30)
        self.show()

        if self.success:

            self.count += 1
            if self.count%20 == 0:
                self.success,self.image = self.vidcap.read()

            h = self.rand(768-self.hstep)
            w = self.rand(1366-self.wstep)
            self.im = self.image[h:h+self.hstep,w:w+self.wstep,:]
            print(type(self.im))

            
            pixmap = self.create_QPixmap()
            self.label.setPixmap(pixmap)
            
            self.textbox.setText(str(self.image_cnt['im_count']))

        else:
            print("No Video Input!")
            self.close_wd()
            return -1

        #self.textbox.setDisabled()


    def save_img(self):

        self.image_label["im_"+str(self.image_cnt['im_count'])] = 1
        s = Image.fromarray(self.im)
        s.save("source/im_"+str(self.image_cnt['im_count'])+".png")
        self.image_cnt['im_count'] += 1
        self.save_json(self.image_cnt,'source/image_count.json')
        self.save_json(self.image_label,'source/image_label.json')

        if self.success:

            self.count += 1
            if self.count%20 == 0:
                self.success,self.image = self.vidcap.read()

            h = self.rand(720-self.hstep)
            w = self.rand(1280-self.wstep)

            self.im = self.image[h:h+self.hstep,w:w+self.wstep,:]



            pixmap = self.create_QPixmap()
            self.label.setPixmap(pixmap)

            self.textbox.setText(str(self.image_cnt['im_count']))


    def save_img2(self):
        self.image_label["im_"+str(self.image_cnt['im_count'])] = 2
        s = Image.fromarray(self.im)
        s.save("source/im_"+str(self.image_cnt['im_count'])+".png")
        self.image_cnt['im_count'] += 1
        self.save_json(self.image_cnt,'source/image_count.json')
        self.save_json(self.image_label,'source/image_label.json')

        if self.success:

            self.count += 1
            if self.count%20 == 0:
                self.success,self.image = self.vidcap.read()

            h = self.rand(720-self.hstep)
            w = self.rand(1280-self.wstep)
            self.im = self.image[h:h+self.hstep,w:w+self.wstep,:]
            print(h,w)
            pixmap = self.create_QPixmap()
            self.label.setPixmap(pixmap)

            self.textbox.setText(str(self.image_cnt['im_count']))


    def passing(self):

        self.save_json(self.image_cnt,'source/image_count.json')
        self.save_json(self.image_label,'source/image_label.json')

        if self.success:

            self.count += 1
            if self.count%20 == 0:
                self.success,self.image = self.vidcap.read()

            h = self.rand(720-self.hstep)
            w = self.rand(1280-self.wstep)
            self.im = self.image[h:h+self.hstep,w:w+self.wstep,:]
            print(h,w)
            pixmap = self.create_QPixmap()
            self.label.setPixmap(pixmap)

            self.textbox.setText(str(self.image_cnt['im_count']))



    def save_json(self,data,path):
        with open(path, 'w') as fp:
            json.dump(data, fp)


    def load_count(self):
        try:
            with open('source/image_count.json', 'r') as fp:
                data = json.load(fp)
                self.image_cnt = data

        except json.decoder.JSONDecodeError:
            data = defaultdict(int)
            data['im_count'] = 0
            data['y'] = []
            self.image_cnt = data

    def load_json(self,path):
        try:
            with open(path, 'r') as fp:
                data = json.load(fp)
                self.image_label = data

        except json.decoder.JSONDecodeError:
            data = defaultdict(int)
            self.image_label = data

    def rand(self,val):
        return int(np.random.rand(1)*val)








if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

