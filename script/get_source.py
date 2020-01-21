from collections import defaultdict
import json, sys
from PIL import Image
import numpy as np
import locating
import time
import key_event as ke
import image_process as ip
import cv2


def save_json(data,path):
    with open(path, 'w') as fp:
        json.dump(data, fp)


def load_count():
    try:
        with open('source/image_count.json', 'r') as fp:
            data = json.load(fp)
            return data
    except json.decoder.JSONDecodeError:
        data = defaultdict(int)
        data['im_count'] = 0
        data['y'] = []
        return data

def load_json(path):
    try:
        with open(path, 'r') as fp:
            data = json.load(fp)
            return data
    except json.decoder.JSONDecodeError:
        data = defaultdict(int)
        return data

def rand(val):
        return int(np.random.rand(1)*val)

def get_source():


    hstep = int(sys.argv[2])
    wstep = int(sys.argv[1])

    #hwnd = ke.get_hwnd('MapleStory')
    #if hwnd == 0:
    #    print("No Maplestory found in Process...")
    #    return -1
    #ke.set_topwnd(hwnd)
    #print(hwnd)

        
    vidcap = cv2.VideoCapture('sample.flv')
    success = True
    count = 0

    try:
        while success:
            success,im = vidcap.read()
            count += 1
            if count%30 != 0:
                continue



            #rem_h = np.remainder(768,hstep)
            #rem_w = np.remainder(1366,wstep)

            #im = ip.image_grab(locating.locate(hwnd,rem_h,rem_w))
            
            #im = ip.rgb2gray(im)
            height,width,_ = im.shape

            print(im.shape)

            

            #cnt = 0
            #sections = np.zeros((int(height/hstep*width/wstep), hstep, wstep))
            sections = np.zeros((20,)+(hstep,)+(wstep,)+(3,))
            #for i in range(0,height,hstep):
            #    for j in range(0,width,wstep):
            for i in range(0,20):
                    #sections[cnt] = im[i:i+hstep,j:j+wstep,:]
                    h = rand(720-hstep)
                    w = rand(1280-wstep)
                    sections[i] = im[h:h+hstep,w:w+wstep,:]

                    #cnt += 1


            image_cnt = load_count()
            image_label = load_json('source/image_label.json')
            print(image_cnt['im_count'])

            for section in sections:

                #val = input("1: Monster   2:Not Monster\n")
                #image_label["im_"+str(image_cnt['im_count'])] = int(val)

                section = cv2.cvtColor(np.uint8(section), cv2.COLOR_BGR2RGB)
                s = Image.fromarray(np.uint8(section))

                s.save("source/im_"+str(image_cnt['im_count'])+".png")

                image_cnt['im_count'] += 1

            save_json(image_cnt,'source/image_count.json')
            save_json(image_label,'source/image_label.json')
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    get_source()