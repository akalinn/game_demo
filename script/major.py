import cv2
import numpy as np
import image_process as ip
import os,re,sys
import win32api, win32gui, win32ui
from ctypes import windll
from PIL import Image, ImageGrab
from PyQt5.QtWidgets import QPushButton,QMainWindow,QApplication,QFileDialog,QCheckBox,qApp
from PyQt5.QtCore import QObject,QThread,pyqtSignal,Qt


class AThread(QObject):

    finished = pyqtSignal()
    update_im_rec = pyqtSignal()
    


    def updt_im_rec(self,pt):


        self.update_im_rec.emit()

    def run(self):

        #while True:
        #    pass

        self.finished.emit()


class MPS(QMainWindow):
    def __init__(self):
        super(MPS,self).__init__()
        self.files = os.listdir('source/')
        self.im_loc = []
        self.not_found = 0 
        #self.files2 = os.listdir('source/')
        #self.vidcap = cv2.VideoCapture('sample.flv')   
        #self.obshwnd = win32gui.FindWindow(None, 'obs64')
        self.obshwnd = win32gui.FindWindow(None, 'OBS 21.1.2 (64bit, windows) - 配置文件: 未命名 - 场景: 未命名')
        
        self.setWindowTitle('MaJor')
        self.setGeometry(200, 200, 250, 150)

        self.objThread = QThread()
        self.obj = AThread()
        self.obj.moveToThread(self.objThread)
        self.obj.finished.connect(self.objThread.quit)
        self.objThread.started.connect(self.obj.run)
        #self.objThread.finished.connect(app.exit)
        self.objThread.start()


        self.InitWindow()


    def InitWindow(self):

        self.setMinimumHeight(150)
        self.setMinimumWidth(250)
        self.setMaximumHeight(150)
        self.setMaximumWidth(250)



        self.b = QCheckBox("Import Video?",self)
        self.b.stateChanged.connect(self.clickBox)
        self.b.move(15,20)
        #self.b.resize(100,30)

        btn1 = QPushButton("Run", self)
        btn1.move(135, 20)
        btn2 = QPushButton("End", self)
        btn2.move(135, 80)

        btn1.clicked.connect(self.c_open_)
        btn2.clicked.connect(qApp.quit)

        self.show()

    def c_open_(self): 
        self.close()
        try:
            print(self.import_video)
            self.major_video()
        except AttributeError:
            self.major()


    def clickBox(self, state):
        self.import_video = Qt.Checked




    def get_data(self,grammar,s):
        re_source = re.compile(grammar)
        return re.search(re_source,s)


    def detect(self,im):

        try:
            gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)   
        except cv2.error:
            pass

        self.im_loc = []
        self.player_loc = []

        for file in self.files:
            
            if self.get_data('player.*?',file):

                temp = cv2.imread('source/'+file,0 )

                h, w = temp.shape

                match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
                loc = np.where( match >= 0.6)

                for pt in zip(*loc[::-1]):
                    pt = [int(pt[0]+w/2),int(pt[1]+h/2)]
                    self.player_loc.append(pt)
                    break
            
            if self.get_data('im_.+?',file):
            

                temp = cv2.imread('source/'+file,0 )

                h, w = temp.shape

                match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
                loc = np.where( match >= 0.8)


                for pt in zip(*loc[::-1]):
                    has_close_point = False
                    for ppt in self.im_loc:
                        if (np.square(pt[0]-ppt[0])+np.square(pt[1]-ppt[1])) < 50:
                            has_close_point = True
                            break
                    if has_close_point == True:
                        continue
                    else:
                        pt = [int(pt[0]+w/2),int(pt[1]+h/2)]
                        self.im_loc.append(pt)


        print(self.im_loc)
        if self.im_loc == []:
            self.not_found += 1
            if self.not_found > 20:
                sys.exit()
            im = self.capture_bitmap()
            self.detect()

        
        self.not_found = 0

    def detect2(self,im):


 
        try:
            gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)   
        except cv2.error:
            pass

        self.im_loc = []
        self.player_loc = []

        for file in self.files:
            
            if self.get_data('player.+?',file):

                temp = cv2.imread('source/'+file,0 )

                h, w = temp.shape

                match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
                loc = np.where( match >= 0.6)

                for pt in zip(*loc[::-1]):
                    self.player_loc.append(pt)
                    cv2.rectangle(im, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                    break
            
            if self.get_data('im_.+?',file):
            

                temp = cv2.imread('source/'+file,0 )

                h, w = temp.shape

                match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
                loc = np.where( match >= 0.8)


                for pt in zip(*loc[::-1]):
                    has_close_point = False
                    for ppt in self.im_loc:
                        if (np.square(pt[0]-ppt[0])+np.square(pt[1]-ppt[1])) < 50:
                            has_close_point = True
                            break
                    if has_close_point == True:
                        continue
                    else:
                        self.im_loc.append(pt)
                    cv2.rectangle(im, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        print(self.not_found)
        if self.im_loc == [] or self.player_loc == []:
            self.not_found += 1
            success,im = self.vidcap.read()
            if self.not_found > 30 or not success:
                sys.exit()

            self.detect2(im)

        
        self.not_found = 0
        cv2.imshow('image', im)

    def create_bitmap(self):

        self.hwndDC = win32gui.GetWindowDC(self.obshwnd)
        self.mfcDC  = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

        left, top, right, bot = win32gui.GetClientRect(self.obshwnd)
        w = right - left
        h = bot - top
        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, w, h)
        self.saveDC.SelectObject(self.saveBitMap)



    def capture_bitmap(self):

        result = windll.user32.PrintWindow(self.obshwnd, self.saveDC.GetSafeHdc(), 0)

        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        if result == 0 or self.obshwnd == 0:
            print("Wrong Hwnd or Cannot Capture image...")
            return -1

        im = np.asarray(im)
        
        #index check keep image 1366x768
        im = im[79:-170,285:-269,:]
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        return im

        #cv2.imshow('image', im)
        #if cv2.waitKey(1) >= 0:  # Break with ESC 
        #    break

    def delete_bitmap(self):

        win32gui.DeleteObject(self.saveBitMap.GetHandle())
        self.saveDC.DeleteDC()
        self.mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.obshwnd, self.hwndDC)


    def major(self):

        self.create_bitmap()

        while True:
            im = self.capture_bitmap()
            self.detect(im)


            if cv2.waitKey(1) >= 0:  # Break with ESC 
                break



        self.delete_bitmap()

    def major_video(self):

        print(cv2.getBuildInformation())

        self.file_name = QFileDialog.getOpenFileName(self, 'Open file', 
            '',"Video files (*.flv *.mp4)")[0]

        self.vidcap = cv2.VideoCapture(self.file_name)  

        success = True

        while success:
            success,im = self.vidcap.read()

            self.detect2(im)

            if cv2.waitKey(1) >= 0:  # Break with ESC 
                break



        
         

if __name__ == "__main__":
    app = QApplication(sys.argv)
    A = MPS()
    sys.exit(app.exec_())
    #A.major()