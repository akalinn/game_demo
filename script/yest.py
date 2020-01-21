import cv2, os, sys
import numpy as np
import image_process as ip
sys.path.insert(0, 'chainer-recognize/')
from model import GoogleNet


def main():
    # 入力画像とテンプレート画像をで取得
    img = cv2.imread("input.png")
    temps = {}
    temps[0] = cv2.imread("MS_Monster_Fairy.png",0 )
    temps[1] = cv2.imread("1.png",0 )
    temps[2] = cv2.imread("2.png",0 )
    temps[3] = cv2.imread("3.png",0 )



    m = GoogleNet()
    m.load("bvlc_googlenet.caffemodel")
    m.load_label("labels.txt")
    m.print_prediction("image.png")


    try:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)   
    except cv2.error:
        pass




    # Capture frame-by-frame
    frame_resized = cv2.resize(gray,(300,300)) # resize frame for prediction
    # MobileNet requires fixed dimensions for input image(s)
    # so we have to ensure that it is resized to 300x300 pixels.
    # set a scale factor to image because network the objects has differents size. 
    # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
    # after executing this command our "blob" now has the shape:
    # (1, 3, 300, 300)
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    #Set to network the input blob 
    net.setInput(blob)
    #Prediction of network
    detections = net.forward()


    #Size of frame resize (300x300)
    cols = frame_resized.shape[1] 
    rows = frame_resized.shape[0]
    #For get the class and location of object detected, 
    # There is a fix index for class, location and confidence
    # value in @detections array .
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2] #Confidence of prediction 
        if confidence > args.thr: # Filter prediction 
            class_id = int(detections[0, 0, i, 1]) # Class label
            # Object location 
            xLeftBottom = int(detections[0, 0, i, 3] * cols) 
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop   = int(detections[0, 0, i, 5] * cols)
            yRightTop   = int(detections[0, 0, i, 6] * rows)



            # Factor for scale to original size of frame
            heightFactor = frame.shape[0]/300.0  
            widthFactor = frame.shape[1]/300.0 
            # Scale object detection to frame
            xLeftBottom = int(widthFactor * xLeftBottom) 
            yLeftBottom = int(heightFactor * yLeftBottom)
            xRightTop   = int(widthFactor * xRightTop)
            yRightTop   = int(heightFactor * yRightTop)
            # Draw location of object  
            cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                          (0, 255, 0))
            # Draw label and confidence of prediction in frame resized
            if class_id in classNames:
                label = classNames[class_id] + ": " + str(confidence)
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                yLeftBottom = max(yLeftBottom, labelSize[1])
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                     (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                     (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                print(label) #print class and confidence 
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) >= 0:  # Break with ESC 
            break

    for i in range(1,len(temps)):


        try:
            temps[i] = cv2.cvtColor(temps[i], cv2.COLOR_RGB2GRAY)   
        except cv2.error:
            pass

        # テンプレート画像の高さ・幅
        h, w = temps[i].shape

        # テンプレートマッチング（OpenCVで実装）
        match = cv2.matchTemplate(gray, temps[i], cv2.TM_CCOEFF_NORMED)
        print(match)
        threshold = 0.7
        loc = np.where( match >= threshold)
        #min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
        #pt = min_pt



        for pt in zip(*loc[::-1]):
        

            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)


    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()