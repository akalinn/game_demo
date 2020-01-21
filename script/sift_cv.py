import cv2
import numpy as np
import image_process as ip
import matplotlib.pyplot as plt
import os


def main():
    # 入力画像とテンプレート画像をで取得
    #temps = load_json("source/image_label.json")
    



    vidcap = cv2.VideoCapture('sample2.flv')
    success = True

    while success:
        success,img = vidcap.read()
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)   
        except cv2.error:
            pass

        #temp = cv2.imread('MS_Monster_Evil_Eye.png',0)
        #temp = cv2.imread('source/im_0.png',0)
        temp = cv2.imread('ttttt.jpg',0)

        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(gray,None)
        kp2, des2 = sift.detectAndCompute(temp,None)
        
        #img=cv2.drawKeypoints(gray,kp1)

        #img=cv2.drawKeypoints(gray,kp1,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #cv2.imwrite('sift_keypoints.jpg',img)
        temp=cv2.drawKeypoints(temp,kp2,temp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite('sift_keypoints2.jpg',temp)
        #pause()




        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        # Apply ratio test
        good = []
        for m,n in matches:
            if m.distance < 0.5*n.distance:
                good.append([m])
        # cv2.drawMatchesKnn expects list of lists as matches.
        img3 = cv2.drawMatchesKnn(gray,kp1,temp,kp2,good,None,flags=2)
        #plt.imshow(img3),plt.show()

        cv2.imshow('image',img3)
        if cv2.waitKey(1) >= 0:  # Break with ESC 
            break
        #pause()


if __name__ == "__main__":
    main()