import cv2
import numpy as np
import image_process as ip
import os



def main():
    # 入力画像とテンプレート画像をで取得
    #temps = load_json("source/image_label.json")
    files = os.listdir('source/')



    vidcap = cv2.VideoCapture('sample2.flv')
    success = True

    while success:
        success,img = vidcap.read()
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)   
        except cv2.error:
            pass

        for file in files:

            if file == 'image_label.json':
                continue

            temp = cv2.imread('source/'+file,0 )

            # テンプレート画像の高さ・幅
            h, w = temp.shape

            # テンプレートマッチング（OpenCVで実装）
            match = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
            #print(match)
            threshold = 0.7
            loc = np.where( match >= threshold)
            #if loc == []:
            #    min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
            #    loc = min_pt


            #match = cv2.matchTemplate(gray, temp, cv2.TM_SQDIFF)
            #min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
            #pt = min_pt  
            #print(min_pt)

            #cv2.rectangle(img, (pt[0], pt[1] ), (pt[0] + w, pt[1] + h), (0,0,200), 3)

            for pt in zip(*loc[::-1]):
            

                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)


        cv2.imshow('image', img)
        if cv2.waitKey(1) >= 0:  # Break with ESC 
            break


if __name__ == "__main__":
    main()